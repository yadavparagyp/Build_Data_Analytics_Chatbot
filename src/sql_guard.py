from __future__ import annotations
import re
import sqlparse

DISALLOWED = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "ATTACH", "DETACH",
    "COPY", "EXPORT", "IMPORT", "CALL", "PRAGMA", "VACUUM"
}

def is_safe_select_sql(sql: str) -> bool:
    # Parse statements and ensure only SELECT / WITH queries
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False

    for stmt in parsed:
        # Flatten tokens and check keywords
        tokens = [t.value.upper() for t in stmt.flatten() if t.value and t.ttype]
        joined = " ".join(tokens)
        # Disallow multiple statements via semicolon patterns
        if ";" in sql.strip().rstrip(";"):
            return False

        for bad in DISALLOWED:
            if re.search(rf"\b{bad}\b", joined):
                return False

        # Must contain SELECT somewhere
        if not re.search(r"\bSELECT\b", joined):
            return False

    return True
