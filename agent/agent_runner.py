# agent/agent_runner.py
"""
Agent runner module that configures and executes the productivity agent.
Handles the setup of the LLM, tools, and streaming of responses.
"""
from typing import Iterator, Dict, Any, Optional
from functools import lru_cache
import logging
from datetime import datetime

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import AzureChatOpenAI
from langsmith import Client

from agent.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    ENABLE_LANGSMITH,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    LANGSMITH_ENDPOINT,
)
from agent.tools import TOOLS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentConfig:
    """Configuration class for the agent."""
    def __init__(self):
        self.temperature = 0.2
        self.max_tokens = 2000
        self.stream_mode = "values"
        self.thread_id = f"chat-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

@lru_cache(maxsize=1)
def get_llm_model() -> AzureChatOpenAI:
    """Get cached instance of AzureChatOpenAI model."""
    try:
        return AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            openai_api_key=AZURE_OPENAI_API_KEY,
            openai_api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.2,
            max_tokens=2000,
        )
    except Exception as e:
        logger.error(f"Failed to initialize AzureChatOpenAI model: {str(e)}")
        raise

@lru_cache(maxsize=1)
def get_agent() -> Any:
    """Get cached instance of the agent."""
    try:
        model = get_llm_model()
        memory = MemorySaver()
        
        # Configure LangSmith if enabled
        if ENABLE_LANGSMITH and LANGSMITH_API_KEY:
            client = Client(
                api_key=LANGSMITH_API_KEY,
                api_url=LANGSMITH_ENDPOINT,
            )
            logger.info("LangSmith tracing is enabled")
        else:
            logger.info("LangSmith tracing is disabled")
            
        return create_react_agent(model, TOOLS, checkpointer=memory)
    except Exception as e:
        logger.error(f"Failed to create agent: {str(e)}")
        raise

def run_agent(user_query: str, config: Optional[AgentConfig] = None) -> Iterator[Dict[str, Any]]:
    """
    Configures and runs the productivity agent with the given user query.
    
    Args:
        user_query: The user's question or command
        config: Optional configuration for the agent
        
    Returns:
        Iterator of agent steps containing response messages
        
    Raises:
        ValueError: If user_query is empty
        Exception: For any other errors during agent execution
    """
    if not user_query.strip():
        raise ValueError("User query cannot be empty")
    
    try:
        # Use provided config or create default
        agent_config = config or AgentConfig()
        
        # Get cached agent instance
        agent = get_agent()
        
        # Configure the agent session
        session_config = {
            "configurable": {
                "thread_id": agent_config.thread_id
            }
        }
        messages = [HumanMessage(content=user_query)]

        # Stream the agent's responses
        for step in agent.stream(
            {"messages": messages}, 
            session_config, 
            stream_mode=agent_config.stream_mode
        ):
            try:
                step["messages"][-1].pretty_print()
                yield step
            except Exception as e:
                logger.error(f"Error processing step: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Agent execution failed: {str(e)}")
        raise