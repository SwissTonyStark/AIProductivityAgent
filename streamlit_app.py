import streamlit as st
import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from agent.tools import TOOLS
from agent.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME,
)

# --- Streamlit page config ---
st.set_page_config(page_title="Productivity Agent", page_icon="🤖", layout="wide")
st.title("🤖 AI Productivity Agent")
st.markdown("Ask me anything about your emails, create calendar events, or work context.")

# --- Initialize agent ---
@st.cache_resource
def initialize_agent():
    model = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    )
    memory = MemorySaver()
    return create_react_agent(model, TOOLS, checkpointer=memory)

agent = initialize_agent()

# --- Input box ---
user_input = st.chat_input("Type your command...")
if user_input:
    st.chat_message("user").write(user_input)

    config = {"configurable": {"thread_id": "streamlit-session-001"}}
    with st.spinner("🤖 Thinking..."):
        for step in agent.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="values",
        ):
            response = step["messages"][-1].content
            st.chat_message("assistant").markdown(response)


# --- Additional Enhancements ---
st.sidebar.title("Assistant Features")
st.sidebar.markdown("""
- **Analyze Emails**: Get the sentiment and tasks from your emails.
- **Create Events**: Add events to Google Calendar directly.
- **Smart Filtering**: Search emails by keyword or sentiment.
""")
