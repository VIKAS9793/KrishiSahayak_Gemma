"""
Utility functions for caching and rate limiting.
"""
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory cache for storing search results
_search_cache: Dict[str, Tuple[Any, float]] = {}
# Track user requests for rate limiting
_user_requests: Dict[str, List[float]] = {}

# Configuration
CACHE_TTL = 3600  # 1 hour in seconds
RATE_LIMIT = 10   # Max requests per minute per user
RATE_WINDOW = 60   # Time window in seconds

def get_cache_key(query: str, top_k: int) -> str:
    """Generate a cache key from query and parameters."""
    return f"{query.lower().strip()}:{top_k}"

def get_cache(query: str, top_k: int) -> Optional[List[str]]:
    """Retrieve a cached search result if it exists and is not expired."""
    cache_key = get_cache_key(query, top_k)
    if cache_key in _search_cache:
        result, timestamp = _search_cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            logger.debug(f"Cache hit for query: {query[:50]}...")
            return result
        logger.debug(f"Cache expired for query: {query[:50]}...")
        del _search_cache[cache_key]
    return None

def set_cache(query: str, top_k: int, result: List[str]) -> None:
    """Store a search result in the cache."""
    cache_key = get_cache_key(query, top_k)
    _search_cache[cache_key] = (result, time.time())
    logger.debug(f"Cached result for query: {query[:50]}...")

def clear_expired_cache() -> None:
    """Remove expired cache entries."""
    current_time = time.time()
    expired_keys = [k for k, (_, t) in _search_cache.items() 
                   if current_time - t >= CACHE_TTL]
    for key in expired_keys:
        del _search_cache[key]
    if expired_keys:
        logger.info(f"Cleared {len(expired_keys)} expired cache entries")

def rate_limit(user_id: str = "default") -> bool:
    """
    Check if a user has exceeded the rate limit.
    Returns True if the request is allowed, False if rate limited.
    """
    current_time = time.time()
    
    # Remove old requests outside the rate limit window
    if user_id in _user_requests:
        _user_requests[user_id] = [
            t for t in _user_requests[user_id] 
            if current_time - t < RATE_WINDOW
        ]
    
    # Check rate limit
    request_count = len(_user_requests.get(user_id, []))
    if request_count >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for user {user_id}")
        return False
    
    # Record this request
    if user_id not in _user_requests:
        _user_requests[user_id] = []
    _user_requests[user_id].append(current_time)
    
    return True

def with_retry(max_retries: int = 3, backoff_factor: float = 0.5):
    """Decorator for adding retry logic to functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    wait_time = backoff_factor * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {wait_time:.2f}s..."
                    )
                    time.sleep(wait_time)
            logger.error(f"All {max_retries} attempts failed")
            raise last_exception
        return wrapper
    return decorator
