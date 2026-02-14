from __future__ import annotations
import pandas as pd

def df_to_markdown(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows returned._"
    show = df.head(max_rows).copy()
    return show.to_markdown(index=False)

def format_answer(question: str, plan: list[str], df: pd.DataFrame, interpretation: str, assumptions: list[str], followups: list[str]) -> str:
    parts = []
    parts.append(f"**Question:** {question}")
    if plan:
        parts.append("**Plan:**\n" + "\n".join([f"- {p}" for p in plan]))
    parts.append("**Result:**\n" + df_to_markdown(df))
    if interpretation:
        parts.append(f"**Interpretation:** {interpretation}")
    if assumptions:
        parts.append("**Assumptions:**\n" + "\n".join([f"- {a}" for a in assumptions]))
    if followups:
        parts.append("**Suggested follow-ups:**\n" + "\n".join([f"- {f}" for f in followups]))
    return "\n\n".join(parts)
