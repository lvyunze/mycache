"""
A bunch of caches.
"""

from mycache.nohashmap import Map
from mycache.cache import Cache
from mycache.decorators import cache


__all__ = ["cache", "Cache", "Map"]
