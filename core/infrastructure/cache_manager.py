"""
Cache manager module for efficient data caching and retrieval.
Implements a multi-level caching system with memory and disk caching.
"""
from typing import Any, Optional, Dict, List
import time
import json
import os
import pickle
from datetime import datetime, timedelta
import logging
from functools import wraps
from pathlib import Path
import threading
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheEntry:
    """Represents a cached item with metadata."""
    
    def __init__(self, key: str, value: Any, ttl: int = 3600):
        """
        Initialize a cache entry.
        
        Args:
            key: Cache key
            value: Cached value
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.ttl = ttl
        self.last_accessed = datetime.now()
        self.access_count = 0
    
    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl)
    
    def access(self) -> None:
        """Update access metadata when entry is accessed."""
        self.last_accessed = datetime.now()
        self.access_count += 1

class CacheManager:
    """Multi-level cache manager with memory and disk caching."""
    
    def __init__(self, cache_dir: str = ".cache"):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir: Directory for disk cache (default: .cache)
        """
        self._memory_cache: Dict[str, CacheEntry] = {}
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)
        self._lock = threading.Lock()
        self._cleanup_threshold = 1000  # Items in memory before cleanup
        
        # Start background cleanup task
        self._setup_cleanup_task()
    
    def _setup_cleanup_task(self):
        """Setup periodic cache cleanup."""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(300)  # Run every 5 minutes
                self.cleanup()
        
        loop = asyncio.get_event_loop()
        loop.create_task(cleanup_loop())
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        # Try memory cache first
        with self._lock:
            if key in self._memory_cache:
                entry = self._memory_cache[key]
                if not entry.is_expired():
                    entry.access()
                    return entry.value
                else:
                    del self._memory_cache[key]
        
        # Try disk cache
        disk_path = self._cache_dir / f"{key}.cache"
        if disk_path.exists():
            try:
                with open(disk_path, 'rb') as f:
                    entry = pickle.load(f)
                if not entry.is_expired():
                    # Move to memory cache
                    self._memory_cache[key] = entry
                    return entry.value
                else:
                    disk_path.unlink()
            except Exception as e:
                logger.error(f"Error reading from disk cache: {str(e)}")
        
        return default
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 1 hour)
        """
        entry = CacheEntry(key, value, ttl)
        
        # Store in memory cache
        with self._lock:
            self._memory_cache[key] = entry
            
            # Check if cleanup needed
            if len(self._memory_cache) > self._cleanup_threshold:
                self.cleanup()
        
        # Store in disk cache
        try:
            disk_path = self._cache_dir / f"{key}.cache"
            with open(disk_path, 'wb') as f:
                pickle.dump(entry, f)
        except Exception as e:
            logger.error(f"Error writing to disk cache: {str(e)}")
    
    def delete(self, key: str) -> None:
        """
        Delete an item from cache.
        
        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._memory_cache:
                del self._memory_cache[key]
        
        disk_path = self._cache_dir / f"{key}.cache"
        if disk_path.exists():
            try:
                disk_path.unlink()
            except Exception as e:
                logger.error(f"Error deleting from disk cache: {str(e)}")
    
    def cleanup(self) -> None:
        """Clean up expired cache entries."""
        # Cleanup memory cache
        with self._lock:
            expired_keys = [
                key for key, entry in self._memory_cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._memory_cache[key]
        
        # Cleanup disk cache
        try:
            for cache_file in self._cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        entry = pickle.load(f)
                    if entry.is_expired():
                        cache_file.unlink()
                except Exception:
                    # If we can't read the cache file, delete it
                    cache_file.unlink()
        except Exception as e:
            logger.error(f"Error during disk cache cleanup: {str(e)}")
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._memory_cache.clear()
        
        try:
            for cache_file in self._cache_dir.glob("*.cache"):
                cache_file.unlink()
        except Exception as e:
            logger.error(f"Error clearing disk cache: {str(e)}")

# Cache decorator
def cached(ttl: int = 3600):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds (default: 1 hour)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache_manager.get(key)
            if result is not None:
                return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl)
            return result
        return wrapper
    return decorator

# Global cache manager instance
cache_manager = CacheManager()

# Example usage:
"""
@cached(ttl=3600)
def expensive_operation(param1, param2):
    # Expensive computation here
    return result

# Or use directly:
cache_manager.set("my_key", "my_value", ttl=3600)
value = cache_manager.get("my_key")
""" 