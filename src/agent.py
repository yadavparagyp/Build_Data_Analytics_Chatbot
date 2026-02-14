from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

import duckdb
import pandas as pd
# from .sql_schema_guard import find_unknown_columns
from .sql_schema_guard import find_unknown_identifiers
from .data_loader import get_table_columns



from .llm_ollama import OllamaClient
from .sql_guard import is_safe_select_sql
from .formatting import format_answer
from .prompts import system_prompt, REFINE_PROMPT
from .schema_reader import TableSchema
from .config import SETTINGS

# @dataclass
# # class ChatState:
# #     # Keep short memory of prior filters / last question intent
# #     last_filters: Dict[str, Any] = field(default_factory=dict)
# #     last_question: Optional[str] = None
# #     last_sql: Optional[str] = None

@dataclass
class ChatState:
    last_filters: Dict[str, Any] = field(default_factory=dict)
    last_question: Optional[str] = None
    last_sql: Optional[str] = None

    # NEW: store resolved entities
    top_city: Optional[str] = None


class AnalyticsAgent:
    def __init__(self, con: duckdb.DuckDBPyConnection, schema: TableSchema):
        self.con = con
        self.schema = schema
        self.llm = OllamaClient()

        self.table_view = f"{SETTINGS.table_name}_v"
        db_cols = get_table_columns(self.con, self.table_view)
        self.valid_identifiers = {c.lower() for c in db_cols} | {SETTINGS.table_name.lower(), self.table_view.lower()}

        self.valid_columns = {c.name.lower() for c in self.schema.columns}
        # self.valid_identifiers = set(self.valid_columns) | {SETTINGS.table_name.lower(), self.table_view.lower()}

        self.sys = system_prompt(
            # schema_text=self.schema.to_prompt_text(),
            schema_text=self.schema.to_compact_prompt_text(),

            table_view=self.table_view,
            max_rows=SETTINGS.max_rows_returned
        )

    def _messages(self, user_question: str, state: ChatState) -> List[Dict[str, str]]:
        # We lightly inject context: last filters + last question
        context = {
            "last_question": state.last_question,
            "last_filters": state.last_filters,
            "note": "If the new question is a follow-up like 'what about Mumbai?', apply those filters on top of last_filters."
        }
        return [
            {"role": "system", "content": self.sys},
            {"role": "user", "content": f"Conversation context JSON:\n{json.dumps(context)}\n\nUser question:\n{user_question}"}
        ]

    def _refine_messages(self, user_question: str, prev_sql: str, error: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.sys},
            {"role": "user", "content": REFINE_PROMPT.strip()},
            {"role": "user", "content": f"User question:\n{user_question}\n\nPrevious SQL:\n{prev_sql}\n\nError/Issue:\n{error}"}
        ]

    def _parse_llm_json(self, text: str) -> Dict[str, Any]:
        # Strict JSON parsing with small cleanup
        cleaned = text.strip()
        return json.loads(cleaned)

    def _apply_default_limit_if_missing(self, sql: str) -> str:
        # If user query results likely multi-row and LIMIT missing, LLM should add it.
        # We'll trust the LLM; but as safety, if no LIMIT found, append one.
        up = sql.upper()
        if "LIMIT" not in up:
            return sql.rstrip() + f"\nLIMIT {SETTINGS.max_rows_returned}"
        return sql

    def _execute(self, sql: str) -> pd.DataFrame:
        return self.con.execute(sql).df()

    def answer(self, user_question: str, state: ChatState) -> Tuple[str, ChatState]:
        q = user_question
        if isinstance(state.top_city, str) and state.top_city.strip() and "top city" in q.lower():
            q = q.replace("that top city", state.top_city).replace("top city", state.top_city)

        # 1) Ask LLM for plan+SQL
        llm_text = self.llm.chat(self._messages(user_question, state) ,temperature=0.1)
        payload = self._parse_llm_json(llm_text)

        plan = payload.get("analysis_plan", [])
        sql = payload.get("sql", "")
        interpretation = payload.get("result_interpretation", "")
        assumptions = payload.get("assumptions", [])
        followups = payload.get("followups", [])

        if not sql or not isinstance(sql, str):
            return ("I couldn't generate SQL for that. Try rephrasing your question with a specific metric/dimension.", state)

        sql = self._apply_default_limit_if_missing(sql)

        # 2) Guardrail: read-only SQL
        if not is_safe_select_sql(sql):
            return ("I generated unsafe SQL (non-SELECT). Please rephrase your request as a read-only analytics question.", state)
        
        # 2.5) Schema guard: prevent hallucinated columns
        # unknown = find_unknown_columns(sql, self.valid_identifiers)

        # unknown = find_unknown_identifiers(sql, self.valid_identifiers)

        # if unknown:
        #     err = f"SQL referenced unknown identifiers/columns: {unknown}. Regenerate using only provided schema."
        #     refine_text = self.llm.chat(self._refine_messages(user_question, sql, err), temperature=0.1)
        #     refined = self._parse_llm_json(refine_text)

        #     sql = self._apply_default_limit_if_missing(refined.get("sql", sql))
        #     plan = refined.get("analysis_plan", plan)
        #     interpretation = refined.get("result_interpretation", interpretation)
        #     assumptions = refined.get("assumptions", assumptions)
        #     followups = refined.get("followups", followups)

        #     if not is_safe_select_sql(sql):
        #         return ("The regenerated SQL isn't safe to run.", state)

        #     # unknown2 = find_unknown_columns(sql, self.valid_identifiers)
        #     unknown2 = find_unknown_identifiers(sql, self.valid_identifiers)

        #     if unknown2:
        #         return (f"I couldn't generate valid SQL. Unknown identifiers still present: {unknown2}", state)

        if not is_safe_select_sql(sql):
            return ("I generated unsafe SQL (non-SELECT). Please rephrase.", state)

        # 3) Execute + reflect retry if needed
        tries = 0
        last_err = None
        df: pd.DataFrame | None = None

        while tries < 3:
            tries += 1
            try:
                df = self._execute(sql)
                break
            except Exception as e:
                last_err = str(e)
                # refine
                refine_text = self.llm.chat(self._refine_messages(user_question, sql, last_err))
                refined = self._parse_llm_json(refine_text)
                sql = self._apply_default_limit_if_missing(refined.get("sql", sql))
                plan = refined.get("analysis_plan", plan)
                interpretation = refined.get("result_interpretation", interpretation)
                assumptions = refined.get("assumptions", assumptions)
                followups = refined.get("followups", followups)

                if not is_safe_select_sql(sql):
                    return ("The refined SQL still isn't safe to run. Please ask a read-only question.", state)

        if df is None:
            return (f"I couldn't run the query due to an error: {last_err}", state)

        # 4) Update conversational state (simple heuristic: store likely filters mentioned)
        # new_state = ChatState(
        #     last_question=user_question,
        #     last_sql=sql,
        #     last_filters=state.last_filters.copy()
        # )
        new_state = ChatState(
            last_question=user_question,
            last_sql=sql,
            last_filters=state.last_filters.copy(),
            top_city=state.top_city)
        
        # If result contains exactly one city, remember it
        if df is not None and not df.empty and "city" in df.columns and len(df) == 1:
            new_state.top_city = str(df.iloc[0]["city"])



        # crude filter extraction from question for follow-ups
        # (you can improve later with a dedicated LLM extraction step)
        qlow = user_question.lower()
        for city in ["mumbai", "delhi", "bangalore", "bengaluru", "pune", "hyderabad", "chennai", "kolkata", "ahmedabad"]:
            if city in qlow:
                new_state.last_filters["city"] = city.title().replace("Bengaluru", "Bangalore")
        for plat in ["web", "app"]:
            if f" {plat}" in qlow or qlow.endswith(plat):
                new_state.last_filters["platform"] = plat

        # 5) Format answer
        answer_text = format_answer(
            question=user_question,
            plan=plan,
            df=df,
            interpretation=interpretation,
            assumptions=assumptions,
            followups=followups
        )
        return answer_text, new_state
