# agent/agent_runner.py
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from agent.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME,
)
from agent.tools import TOOLS


def run_agent(user_query: str):
    model = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    )

    memory = MemorySaver()
    agent = create_react_agent(model, TOOLS, checkpointer=memory)

    config = {"configurable": {"thread_id": "gmail-chat-001"}}

    messages = [HumanMessage(content=user_query)]

    for step in agent.stream({"messages": messages}, config, stream_mode="values"):
        step["messages"][-1].pretty_print()
