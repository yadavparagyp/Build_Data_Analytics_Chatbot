from __future__ import annotations
import duckdb
import pandas as pd
from typing import Tuple
from .config import SETTINGS


def debug_date_parse(con: duckdb.DuckDBPyConnection, table_view: str):
    return con.execute(f"""
        SELECT
          MIN(date) AS min_raw_date,
          MAX(date) AS max_raw_date,
          MIN(date_parsed) AS min_date,
          MAX(date_parsed) AS max_date,
          SUM(CASE WHEN date_parsed IS NULL THEN 1 ELSE 0 END) AS null_parsed
        FROM {table_view};
    """).df()


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(database=SETTINGS.duckdb_path)

def load_json_to_duckdb(con: duckdb.DuckDBPyConnection, table_name: str, json_path: str) -> None:
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT * FROM read_json_auto('{json_path}', sample_size=-1);
    """)

    # Robust date parsing: handles 'YYYY-MM-DD', 'YYYY/MM/DD', timestamps, etc.
    con.execute(f"""
        CREATE OR REPLACE VIEW {table_name}_v AS
        SELECT
            *,
            COALESCE(
                TRY_CAST(date AS DATE),
                TRY_STRPTIME(CAST(date AS VARCHAR), '%Y-%m-%d')::DATE,
                TRY_STRPTIME(CAST(date AS VARCHAR), '%Y/%m/%d')::DATE,
                TRY_STRPTIME(SUBSTR(CAST(date AS VARCHAR), 1, 10), '%Y-%m-%d')::DATE,
                TRY_STRPTIME(SUBSTR(CAST(date AS VARCHAR), 1, 10), '%Y/%m/%d')::DATE
            ) AS date_parsed
        FROM {table_name};
    """)


def init_db() -> duckdb.DuckDBPyConnection:
    con = get_connection()
    load_json_to_duckdb(con, SETTINGS.table_name, SETTINGS.data_path)
    return con

def quick_profile(con: duckdb.DuckDBPyConnection, table_name: str) -> pd.DataFrame:
    return con.execute(f"SELECT COUNT(*) AS rows FROM {table_name};").df()

def get_table_columns(con, table_or_view: str) -> list[str]:
    df = con.execute(f"DESCRIBE {table_or_view}").df()
    # DuckDB DESCRIBE output column name is usually 'column_name'
    col = "column_name" if "column_name" in df.columns else df.columns[0]
    return [str(x) for x in df[col].tolist()]
