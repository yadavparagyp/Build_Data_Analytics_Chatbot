from __future__ import annotations
import re
from typing import Set, List

SQL_KEYWORDS = {
    # core
    "select","from","where","group","by","order","limit","having","with","as",
    "and","or","not","null","is","in","on","join","left","right","inner","outer",
    "case","when","then","else","end","distinct","desc","asc",

    # aggregates / functions commonly used
    "count","sum","avg","min","max","nullif","coalesce","try_cast","cast",
    "try_strptime","substr","date","date_trunc",

    # interval/time units that get tokenized as identifiers
    "interval","day","days","week","weeks","month","months","year","years",
}

def _lower_set(xs: Set[str]) -> Set[str]:
    return {x.lower() for x in xs}

def extract_identifiers(sql: str) -> Set[str]:
    """
    Lightweight identifier extraction (case-insensitive).
    We'll later subtract keywords and add aliases/cte names into allowed set.
    """
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sql)
    return {t.lower() for t in tokens}

def extract_aliases_and_ctes(sql: str) -> Set[str]:
    """
    Collect identifiers that should be allowed even if not in schema:
    - CTE names: WITH cte_name AS (...)
    - Aliases: ... AS alias
    - Table aliases: FROM table_name alias / FROM table_name AS alias
    """
    s = sql

    aliases: Set[str] = set()

    # CTE names: WITH name AS
    for m in re.finditer(r"\bwith\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as\b", s, flags=re.IGNORECASE):
        aliases.add(m.group(1).lower())

    # AS aliases: AS name
    for m in re.finditer(r"\bas\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", s, flags=re.IGNORECASE):
        aliases.add(m.group(1).lower())

    # FROM table alias  (no AS)
    for m in re.finditer(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", s, flags=re.IGNORECASE):
        aliases.add(m.group(2).lower())

    # JOIN table alias (no AS)
    for m in re.finditer(r"\bjoin\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", s, flags=re.IGNORECASE):
        aliases.add(m.group(2).lower())

    return aliases

def find_unknown_identifiers(sql: str, valid_identifiers: Set[str]) -> List[str]:
    """
    Return unknown identifiers (case-insensitive), excluding:
    - SQL keywords/functions
    - aliases and cte names
    """
    ids = extract_identifiers(sql)
    allowed = _lower_set(valid_identifiers) | SQL_KEYWORDS | extract_aliases_and_ctes(sql)

    # Filter obvious non-schema tokens (numbers etc. already excluded)
    unknown = sorted({t for t in ids if t not in allowed})
    return unknown
