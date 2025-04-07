"""
API manager module for handling API access, rate limiting, and security.
Provides a unified interface for all external API interactions.
"""
from typing import Dict, Any, Optional, Callable
import time
import json
import logging
import asyncio
from datetime import datetime, timedelta
from functools import wraps
import jwt
import aiohttp
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiScope(Enum):
    """API access scopes."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

@dataclass
class ApiConfig:
    """API configuration settings."""
    base_url: str
    api_key: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    scopes: Optional[list] = None
    rate_limit: int = 60  # requests per minute
    timeout: int = 30  # seconds

class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, calls: int, period: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            calls: Number of calls allowed
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps = []
    
    async def acquire(self) -> bool:
        """
        Try to acquire a rate limit token.
        
        Returns:
            bool: True if acquired, False if rate limited
        """
        now = time.time()
        
        # Remove old timestamps
        self.timestamps = [ts for ts in self.timestamps if ts > now - self.period]
        
        if len(self.timestamps) < self.calls:
            self.timestamps.append(now)
            return True
        
        return False

class ApiManager:
    """Manages API access and authentication."""
    
    def __init__(self):
        """Initialize API manager."""
        self.configs: Dict[str, ApiConfig] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.tokens: Dict[str, Dict[str, Any]] = {}
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize aiohttp session."""
        if not self._session:
            self._session = aiohttp.ClientSession()
    
    async def close(self):
        """Close aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None
    
    def register_api(self, name: str, config: ApiConfig) -> None:
        """
        Register a new API configuration.
        
        Args:
            name: API name
            config: API configuration
        """
        self.configs[name] = config
        self.rate_limiters[name] = RateLimiter(config.rate_limit)
        logger.info(f"Registered API: {name}")
    
    async def get_token(self, api_name: str) -> Optional[str]:
        """
        Get authentication token for API.
        
        Args:
            api_name: Name of the API
            
        Returns:
            Optional[str]: Authentication token if available
        """
        if api_name not in self.tokens:
            await self._authenticate(api_name)
        
        token_info = self.tokens.get(api_name)
        if not token_info:
            return None
        
        # Check if token is expired
        if datetime.now() > token_info['expires_at']:
            await self._authenticate(api_name)
            token_info = self.tokens.get(api_name)
        
        return token_info.get('token') if token_info else None
    
    async def _authenticate(self, api_name: str) -> None:
        """
        Authenticate with an API.
        
        Args:
            api_name: Name of the API
        """
        config = self.configs.get(api_name)
        if not config:
            raise ValueError(f"Unknown API: {api_name}")
        
        if config.client_id and config.client_secret:
            # OAuth2 authentication
            auth_data = {
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'grant_type': 'client_credentials',
                'scope': ' '.join(config.scopes) if config.scopes else ''
            }
            
            async with self._session.post(
                f"{config.base_url}/oauth/token",
                data=auth_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.tokens[api_name] = {
                        'token': data['access_token'],
                        'expires_at': datetime.now() + timedelta(seconds=data['expires_in'])
                    }
        elif config.api_key:
            # API key authentication
            self.tokens[api_name] = {
                'token': config.api_key,
                'expires_at': datetime.now() + timedelta(days=365)  # Long expiration for API keys
            }
    
    async def request(
        self,
        api_name: str,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Any:
        """
        Make an API request.
        
        Args:
            api_name: Name of the API
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            API response
        """
        if not self._session:
            await self.initialize()
        
        config = self.configs.get(api_name)
        if not config:
            raise ValueError(f"Unknown API: {api_name}")
        
        # Check rate limit
        if not await self.rate_limiters[api_name].acquire():
            raise Exception("Rate limit exceeded")
        
        # Get authentication token
        token = await self.get_token(api_name)
        
        # Prepare headers
        request_headers = headers or {}
        if token:
            request_headers['Authorization'] = f"Bearer {token}"
        
        # Make request
        try:
            url = f"{config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            async with self._session.request(
                method,
                url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=config.timeout
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

# API request decorator
def api_request(api_name: str, method: str, endpoint: str):
    """
    Decorator for API requests.
    
    Args:
        api_name: Name of the API
        method: HTTP method
        endpoint: API endpoint
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await api_manager.request(api_name, method, endpoint, **kwargs)
            except Exception as e:
                logger.error(f"API request failed: {str(e)}")
                raise
        return wrapper
    return decorator

# Global API manager instance
api_manager = ApiManager()

# Example usage:
"""
# Register an API
config = ApiConfig(
    base_url="https://api.example.com",
    api_key="your-api-key",
    rate_limit=60
)
api_manager.register_api("example_api", config)

# Use the decorator
@api_request("example_api", "GET", "/users")
async def get_users(user_id: int):
    return await api_manager.request(
        "example_api",
        "GET",
        f"/users/{user_id}"
    )

# Or use directly
response = await api_manager.request(
    "example_api",
    "GET",
    "/users",
    params={"page": 1}
)
""" 