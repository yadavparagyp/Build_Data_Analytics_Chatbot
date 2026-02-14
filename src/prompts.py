SQL_JSON_SPEC = r"""
Return ONLY valid JSON (no markdown) with this shape:
{{
  "analysis_plan": ["..."],
  "sql": "WITH ... SELECT ...",
  "result_interpretation": "...",
  "assumptions": ["..."],
  "followups": ["..."]
}}

Rules:
- Use ONLY the available table/view names and columns.
- Prefer querying the view {table_view} which includes date_parsed.
- For "last N days": filter date_parsed >= (SELECT MAX(date_parsed) FROM {table_view}) - INTERVAL '{max_days} days'
- Always protect division with NULLIF.
- ALWAYS exclude NULL/empty dimension values in GROUP BY queries (e.g., city IS NOT NULL AND city <> '').
- If asked "Which X has the highest ...", return ONLY the top 1 row using ORDER BY ... DESC LIMIT 1.
- Always include a LIMIT {max_rows} unless the query returns exactly 1 row.
- Never use write operations (no CREATE/DROP/INSERT/UPDATE/DELETE).
"""



def system_prompt(schema_text: str, table_view: str, max_rows: int) -> str:
    return f"""
You are an expert analytics agent. You answer questions by generating DuckDB SQL and interpreting results.

Available schema:
{schema_text}

You MUST follow this output contract:
{SQL_JSON_SPEC.format(table_view=table_view, max_rows=max_rows, max_days=400)}

Business metric definitions (use when relevant):
- D0 Conversion Rate = SUM(d0_orders) / NULLIF(SUM(d0_form_filled), 0)
- Dplus Conversion Rate = SUM(dplus_orders) / NULLIF(SUM(dplus_form_filled), 0)
- Form Completion Rate = SUM(total_form_filled) / NULLIF(SUM(total_form_start), 0)

Output style rules:
- analysis_plan must have 2-4 short bullet items, not placeholders like "step1".
- result_interpretation should be 1-2 lines max.
""".strip()


# REFINE_PROMPT = """
# The previous SQL failed or returned unusable output.

# Given:
# 1) The user's question
# 2) The previous SQL
# 3) The error message OR why the output is unusable

# Return ONLY valid JSON in the same format, with a corrected SQL.
# """

REFINE_PROMPT = """
The previous SQL failed or returned unusable output.

Given:
1) The user's question
2) The previous SQL
3) The error message OR why the output is unusable

Return ONLY valid JSON in the same format, with a corrected SQL.

Rules:
- Ensure SQL is complete and syntactically valid (all parentheses closed, no trailing WITH).
"""

