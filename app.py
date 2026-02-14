import streamlit as st

from src.data_loader import init_db
from src.schema_reader import read_schema
from src.agent import AnalyticsAgent, ChatState
from src.config import SETTINGS

st.set_page_config(page_title="Funnel Analytics Chatbot", layout="wide")
st.title("🧠 Funnel Analytics Chatbot (DuckDB + Ollama)")

@st.cache_resource
def boot():
    con = init_db()
    schema = read_schema(SETTINGS.schema_path, SETTINGS.table_name)
    agent = AnalyticsAgent(con, schema)
    return agent

agent = boot()

if "state" not in st.session_state:
    st.session_state.state = ChatState()
if "chat" not in st.session_state:
    st.session_state.chat = []

with st.sidebar:
    st.subheader("Settings")
    st.write(f"**Model:** {SETTINGS.ollama_model}")
    st.write(f"**Table:** {SETTINGS.table_name}_v")
    st.write(f"**Max rows returned:** {SETTINGS.max_rows_returned}")
    if st.button("Reset conversation"):
        st.session_state.state = ChatState()
        st.session_state.chat = []
        st.rerun()

st.divider()

# Render history
for role, content in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(content)

# Input
user_q = st.chat_input("Ask anything about the funnel data (e.g., 'Which city has highest D0 conversion rate last 15 days?')")

if user_q:
    st.session_state.chat.append(("user", user_q))
    with st.chat_message("user"):
        st.markdown(user_q)

    with st.chat_message("assistant"):
        try:
            answer, new_state = agent.answer(user_q, st.session_state.state)
            st.session_state.state = new_state
            st.markdown(answer)
            st.session_state.chat.append(("assistant", answer))
        except Exception as e:
            err = f"Something went wrong: {e}"
            st.markdown(err)
            st.session_state.chat.append(("assistant", err))
