"""
Configuration and fixtures for pytest.
"""
import pytest
import os
from unittest.mock import MagicMock
from core.infrastructure import ApiManager, CacheManager, EventBus

@pytest.fixture
def mock_azure_credentials():
    """Mock Azure OpenAI credentials."""
    return {
        "api_key": "test_key",
        "endpoint": "https://test.openai.azure.com",
        "api_version": "2024-12-01",
        "deployment_name": "test-deployment"
    }

@pytest.fixture
def mock_api_manager():
    """Mock API manager instance."""
    manager = ApiManager()
    manager.request = MagicMock()
    return manager

@pytest.fixture
def mock_cache_manager():
    """Mock cache manager instance."""
    return CacheManager(cache_dir=".test_cache")

@pytest.fixture
def mock_event_bus():
    """Mock event bus instance."""
    return EventBus()

@pytest.fixture(autouse=True)
def cleanup_test_cache():
    """Clean up test cache after each test."""
    yield
    if os.path.exists(".test_cache"):
        for file in os.listdir(".test_cache"):
            os.remove(os.path.join(".test_cache", file))
        os.rmdir(".test_cache") 