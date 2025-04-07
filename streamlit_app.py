import streamlit as st
import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from agent.tools import TOOLS
from agent.auth_manager import AuthManager

# --- Streamlit page config ---
st.set_page_config(page_title="Productivity Agent", page_icon="🤖", layout="wide")
st.title("🤖 AI Productivity Agent")
st.markdown("Ask me anything about your emails, create calendar events, or work context.")

# Initialize authentication manager
@st.cache_resource
def get_auth_manager():
    return AuthManager()

auth_manager = get_auth_manager()

# --- Initialize agent ---
@st.cache_resource
def initialize_agent():
    # Authenticate all services
    if not auth_manager.authenticate_all():
        st.error("Failed to authenticate services. Please check your credentials and try again.")
        st.stop()
    
    # Initialize Azure OpenAI model
    azure_config = auth_manager.get_azure_openai_config()
    model = AzureChatOpenAI(
        azure_endpoint=azure_config["endpoint"],
        openai_api_key=azure_config["api_key"],
        openai_api_version=azure_config["api_version"],
        azure_deployment=azure_config["deployment_name"],
        temperature=0.2,
    )
    memory = MemorySaver()
    return create_react_agent(model, TOOLS, checkpointer=memory)

# Initialize the agent (this will trigger authentication)
with st.spinner("Initializing services..."):
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
