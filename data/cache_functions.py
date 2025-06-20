"""cache_functions"""

from functools import cache
from typing import Callable

cached_functions = []


def track_cache(func: Callable):
    """Caches the given function and adds it to a list of cached functions.

    Args:
        func (Callable): The function to be cached.

    Returns:
        function: The cached version of the provided function.
    """
    cached_func = cache(func)
    cached_functions.append(cached_func)
    return cached_func


def clear_cache():
    """Clears the cache for all functions that have been cached and are contained in the global
    cached_functions' list."""
    for cached_function in cached_functions:
        cached_function.cache_clear()
