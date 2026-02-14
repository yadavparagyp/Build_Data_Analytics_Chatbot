from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict, List

@dataclass(frozen=True)
class ColumnInfo:
    name: str
    dtype: str
    description: str | None = None

@dataclass(frozen=True)
class TableSchema:
    table_name: str
    columns: List[ColumnInfo]

    def to_prompt_text(self) -> str:
        lines = [f"Table: {self.table_name}", "Columns:"]
        for c in self.columns:
            desc = f" - {c.description}" if c.description else ""
            lines.append(f"- {c.name} ({c.dtype}){desc}")
        return "\n".join(lines)

    # MUST be inside the class
    def to_compact_prompt_text(self, important_only: bool = True) -> str:
        important = {
            "date","gender","platform","city","stage","age_bucket",
            "first_form_utm_medium","first_form_utm_campaign","first_form_utm_source",
            "order_utm_medium","order_utm_campaign","order_utm_source",
            "total_form_start","d0_form_start","total_form_filled","d0_form_filled","dplus_form_filled",
            "d0_orders","dplus_orders","d1_orders","d7_orders","d15_orders","d21_orders","d30_orders","d30plus_orders",
            "NF_orders","d0_revenue"
        }
        cols = self.columns
        if important_only:
            cols = [c for c in self.columns if c.name in important]

        lines = [f"Table: {self.table_name}", "Columns:"]
        for c in cols:
            lines.append(f"- {c.name} ({c.dtype})")
        return "\n".join(lines)

def _try_parse_json_schema(raw: str) -> Dict[str, Any] | None:
    try:
        return json.loads(raw)
    except Exception:
        return None

def read_schema(schema_path: str, table_name: str) -> TableSchema:
    p = Path(schema_path)
    raw = p.read_text(encoding="utf-8")

    js = _try_parse_json_schema(raw)
    if js and isinstance(js, dict):
        cols: List[ColumnInfo] = []

        if "fields" in js and isinstance(js["fields"], list):
            for f in js["fields"]:
                cols.append(
                    ColumnInfo(
                        name=str(f.get("name")),
                        dtype=str(f.get("type", "unknown")),
                        description=f.get("description"),
                    )
                )
            return TableSchema(table_name=table_name, columns=cols)

        if "columns" in js and isinstance(js["columns"], dict):
            for k, v in js["columns"].items():
                cols.append(ColumnInfo(name=str(k), dtype=str(v)))
            return TableSchema(table_name=table_name, columns=cols)

    # Fallback: treat schema as plain text
    cols: List[ColumnInfo] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            left, right = line.split(":", 1)
            name = left.strip().strip("`")
            dtype = right.strip()
            if name and dtype:
                cols.append(ColumnInfo(name=name, dtype=dtype))

    if not cols:
        cols = [ColumnInfo(name="(schema_unavailable)", dtype="text")]

    return TableSchema(table_name=table_name, columns=cols)
