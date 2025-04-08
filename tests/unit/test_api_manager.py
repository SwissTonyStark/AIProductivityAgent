"""
Unit tests for the API Manager component.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from core.infrastructure import ApiManager, ApiConfig, ApiScope

@pytest.mark.asyncio
async def test_api_registration():
    """Test API registration functionality."""
    manager = ApiManager()
    config = ApiConfig(
        base_url="https://api.test.com",
        api_key="test_key",
        rate_limit=60
    )
    
    manager.register_api("test_api", config)
    assert "test_api" in manager.configs
    assert manager.configs["test_api"].api_key == "test_key"
    assert manager.rate_limiters["test_api"] is not None

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting functionality."""
    manager = ApiManager()
    config = ApiConfig(
        base_url="https://api.test.com",
        api_key="test_key",
        rate_limit=2  # Set low for testing
    )
    
    manager.register_api("test_api", config)
    
    # First two requests should succeed
    assert await manager.rate_limiters["test_api"].acquire()
    assert await manager.rate_limiters["test_api"].acquire()
    
    # Third request should be rate limited
    assert not await manager.rate_limiters["test_api"].acquire()

@pytest.mark.asyncio
async def test_token_management():
    """Test token management functionality."""
    manager = ApiManager()
    config = ApiConfig(
        base_url="https://api.test.com",
        api_key="test_key"
    )
    
    manager.register_api("test_api", config)
    token = await manager.get_token("test_api")
    
    assert token == "test_key"
    assert "test_api" in manager.tokens
    assert manager.tokens["test_api"]["token"] == "test_key"

@pytest.mark.asyncio
async def test_token_expiration():
    """Test token expiration handling."""
    manager = ApiManager()
    config = ApiConfig(
        base_url="https://api.test.com",
        client_id="test_client",
        client_secret="test_secret"
    )
    
    manager.register_api("test_api", config)
    
    # Simulate expired token
    manager.tokens["test_api"] = {
        "token": "expired_token",
        "expires_at": datetime.now() - timedelta(hours=1)
    }
    
    # Mock authentication response
    async def mock_authenticate(api_name):
        manager.tokens[api_name] = {
            "token": "new_token",
            "expires_at": datetime.now() + timedelta(hours=1)
        }
    
    manager._authenticate = mock_authenticate
    token = await manager.get_token("test_api")
    
    assert token == "new_token" 