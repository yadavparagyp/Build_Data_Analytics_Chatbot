from src.data_loader import init_db
from src.schema_reader import read_schema
from src.agent import AnalyticsAgent, ChatState
from src.config import SETTINGS

def main():
    con = init_db()
    schema = read_schema(SETTINGS.schema_path, SETTINGS.table_name)
    agent = AnalyticsAgent(con, schema)
    state = ChatState()

    print("Funnel Analytics Chatbot (DuckDB + Ollama). Type 'exit' to quit.")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        ans, state = agent.answer(q, state)
        print("\nAssistant:\n", ans)

if __name__ == "__main__":
    main()
