# agent/agent_runner.py
"""
Agent runner module that configures and executes the productivity agent.
Handles the setup of the LLM, tools, and streaming of responses.
"""
from typing import Iterator, Dict, Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import AzureChatOpenAI

from agent.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME,
)
from agent.tools import TOOLS


def run_agent(user_query: str) -> Iterator[Dict[str, Any]]:
    """
    Configures and runs the productivity agent with the given user query.
    
    Args:
        user_query: The user's question or command
        
    Returns:
        Iterator of agent steps containing response messages
    """
    # Initialize the Azure OpenAI model
    model = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=0.2,  # Lower temperature for more deterministic responses
    )

    # Set up memory and create the agent
    memory = MemorySaver()
    agent = create_react_agent(model, TOOLS, checkpointer=memory)

    # Configure the agent session
    config = {"configurable": {"thread_id": "gmail-chat-001"}}
    messages = [HumanMessage(content=user_query)]

    # Stream the agent's responses
    for step in agent.stream({"messages": messages}, config, stream_mode="values"):
        step["messages"][-1].pretty_print()
        yield step
