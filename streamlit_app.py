import streamlit as st
import os
import random
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from agent.tools import TOOLS
from agent.auth_manager import AuthManager
from agent.agent_runner import run_agent
from agent.config import toggle_langsmith, is_langsmith_enabled

# --- Streamlit page config ---
st.set_page_config(
    page_title="Productivity Agent",
    page_icon="��",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Main app */
    .stApp {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #252526;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #E0E0E0 !important;
    }
    
    /* Feature cards */
    .feature-card {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #3E3E3E;
    }
    
    /* Status badges */
    .status-badge {
        background-color: #2D2D2D;
        color: #E0E0E0;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 5px;
        border: 1px solid #3E3E3E;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-badge.connected {
        border-color: #4CAF50;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: rgba(0, 198, 255, 0.05) !important;
        border: 1px solid #2D2D2D !important;
        color: #E0E0E0 !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        width: 100% !important;
        margin: 5px 0 !important;
        font-size: 1em !important;
    }
    
    .stButton > button:hover {
        background: rgba(0, 198, 255, 0.1) !important;
        border-color: #00C6FF !important;
        box-shadow: 0 4px 12px rgba(0, 198, 255, 0.1) !important;
    }

    /* Grid spacing */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Example prompts
EXAMPLE_PROMPTS = [
    "What are my upcoming meetings today?",
    "Summarize my recent emails about project updates",
    "Create a calendar event for team meeting tomorrow at 2 PM",
    "Find emails from John about the quarterly report",
    "What tasks do I have pending?",
    "Analyze the sentiment of my last 5 emails"
]

# --- Sidebar ---
with st.sidebar:
    # Modern logo and branding
    st.markdown("""
        <div style='display: flex; align-items: center; margin-bottom: 25px; padding: 15px 10px;'>
            <div style='background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 15px; box-shadow: 0 4px 12px rgba(0, 198, 255, 0.2);'>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 3L20 7.5V16.5L12 21L4 16.5V7.5L12 3Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 8L16 10.5V15.5L12 18L8 15.5V10.5L12 8Z" fill="white"/>
                </svg>
            </div>
            <div>
                <div style='font-size: 1.4em; font-weight: 600; color: #E0E0E0; margin-bottom: 2px;'>TaskMind AI</div>
                <div style='font-size: 0.8em; color: #888888;'>Intelligent Productivity</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #888888; font-size: 1.2em; margin: 20px 0;'>Quick Actions</p>", unsafe_allow_html=True)
    
    # Email Management Section
    st.markdown("""
        <div style='margin: 20px 0;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 1.2em; margin-right: 8px;'>📧</span>
                <span style='font-size: 1.2em; color: #E0E0E0;'>Email Management</span>
            </div>
            <div style='margin-left: 28px; color: #888888;'>
                • Search and filter emails<br>
                • Analyze email sentiment<br>
                • Extract tasks from emails
            </div>
        </div>
        <div style='height: 1px; background: #3E3E3E; margin: 20px 0;'></div>
    """, unsafe_allow_html=True)
    
    # Calendar Section
    st.markdown("""
        <div style='margin: 20px 0;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 1.2em; margin-right: 8px;'>📅</span>
                <span style='font-size: 1.2em; color: #E0E0E0;'>Calendar</span>
            </div>
            <div style='margin-left: 28px; color: #888888;'>
                • View upcoming events<br>
                • Create new events<br>
                • Set reminders
            </div>
        </div>
        <div style='height: 1px; background: #3E3E3E; margin: 20px 0;'></div>
    """, unsafe_allow_html=True)
    
    # Task Management Section
    st.markdown("""
        <div style='margin: 20px 0;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 1.2em; margin-right: 8px;'>✅</span>
                <span style='font-size: 1.2em; color: #E0E0E0;'>Task Management</span>
            </div>
            <div style='margin-left: 28px; color: #888888;'>
                • Track pending tasks<br>
                • Set priorities<br>
                • Get task summaries
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Main content ---
st.markdown("""
    <div style='text-align: center; padding: 20px 0 40px 0;'>
        <h1 style='font-size: 2.5em; font-weight: 600; margin: 0; padding: 0;'>TaskMind AI</h1>
        <div style='height: 10px;'></div>
        <p style='font-size: 1.1em; color: #888888; margin: 0; padding: 0;'>Your intelligent AI assistant for seamless productivity</p>
    </div>
""", unsafe_allow_html=True)

# Status badges with updated styling
st.markdown("""
    <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;'>
        <div class='status-badge connected' style='background: rgba(0, 198, 255, 0.1); border-color: #00C6FF;'>
            <span>📧</span><span>Gmail Connected</span>
        </div>
        <div class='status-badge connected' style='background: rgba(0, 198, 255, 0.1); border-color: #00C6FF;'>
            <span>📅</span><span>Calendar Connected</span>
        </div>
        <div class='status-badge connected' style='background: rgba(0, 198, 255, 0.1); border-color: #00C6FF;'>
            <span>🤖</span><span>AI Ready</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize authentication manager
@st.cache_resource
def get_auth_manager():
    return AuthManager()

auth_manager = get_auth_manager()

# Initialize agent
@st.cache_resource
def initialize_agent():
    if not auth_manager.authenticate_all():
        st.error("Failed to authenticate services. Please check your credentials and try again.")
        st.stop()
    
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

# Initialize the agent
with st.spinner("Initializing services..."):
    agent = initialize_agent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Example prompts section
st.markdown("<div style='color: #888888; margin: 30px 0 20px 0; font-size: 1.2em;'>Try asking me:</div>", unsafe_allow_html=True)

# Create columns for the grid
cols = st.columns(3)

# Function to handle prompt selection
def handle_prompt(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    config = {"configurable": {"thread_id": f"streamlit-session-{random.randint(1000, 9999)}"}}
    with st.spinner("🤖 Thinking..."):
        for step in agent.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config,
            stream_mode="values",
        ):
            response = step["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

# Display prompts in grid
for i, prompt in enumerate(EXAMPLE_PROMPTS):
    with cols[i % 3]:
        # Use a unique key for each button based on both index and prompt content
        key = f"prompt_{i}_{hash(prompt)}"
        if st.button(
            prompt,
            key=key,
            use_container_width=True,
            type="secondary"
        ):
            handle_prompt(prompt)

# Chat input
user_input = st.chat_input(
    "Ask me anything about your emails, calendar, or tasks...",
    key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {"configurable": {"thread_id": f"streamlit-session-{random.randint(1000, 9999)}"}}
    with st.spinner("🤖 Thinking..."):
        for step in agent.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="values",
        ):
            response = step["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
