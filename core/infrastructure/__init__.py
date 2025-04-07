"""
Core infrastructure package initialization.
Provides centralized access to all infrastructure components.
"""
from .event_system import (
    EventBus,
    Event,
    EventPriority,
    EventTypes,
    event_bus
)
from .cache_manager import (
    CacheManager,
    CacheEntry,
    cached,
    cache_manager
)
from .api_manager import (
    ApiManager,
    ApiConfig,
    ApiScope,
    RateLimiter,
    api_request,
    api_manager
)

__all__ = [
    # Event System
    'EventBus',
    'Event',
    'EventPriority',
    'EventTypes',
    'event_bus',
    
    # Cache Manager
    'CacheManager',
    'CacheEntry',
    'cached',
    'cache_manager',
    
    # API Manager
    'ApiManager',
    'ApiConfig',
    'ApiScope',
    'RateLimiter',
    'api_request',
    'api_manager'
]

# Version info
__version__ = '0.1.0'
__author__ = 'Pol Fernández'
__email__ = 'pol.fernandez.blanquez@gmail.com' 