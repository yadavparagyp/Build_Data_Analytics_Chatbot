from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    duckdb_path: str = os.getenv("DUCKDB_PATH", ":memory:")
    data_path: str = os.getenv("DATA_PATH", "data/d0_dplus_daily_summary/d0_dplus_daily_summary.json")
    schema_path: str = os.getenv("SCHEMA_PATH", "schemas/d0_dplus_daily_summary.schema")
    table_name: str = os.getenv("TABLE_NAME", "d0_dplus_daily_summary")
    max_rows_returned: int = int(os.getenv("MAX_ROWS_RETURNED", "200"))

SETTINGS = Settings()
