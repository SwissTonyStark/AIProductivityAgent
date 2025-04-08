# agent/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LangSmith - Set to False to disable LangSmith completely
ENABLE_LANGSMITH = False

# LangSmith configuration (only used if ENABLE_LANGSMITH is True)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")

# Global variable to control LangSmith tracing
langsmith_enabled = False

def toggle_langsmith(enabled: bool) -> None:
    """
    Toggle LangSmith tracing on/off.
    
    Args:
        enabled: Boolean to enable/disable LangSmith tracing
    """
    global langsmith_enabled
    langsmith_enabled = enabled

def is_langsmith_enabled() -> bool:
    """
    Check if LangSmith tracing is enabled.
    
    Returns:
        bool: True if LangSmith is enabled, False otherwise
    """
    return langsmith_enabled and bool(LANGSMITH_API_KEY)