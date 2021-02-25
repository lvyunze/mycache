"""
Some useful caching decorators.
"""

from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional

from mycache.cache import Cache


Fany = Callable[..., Any]
Decorator = Callable[[Fany], Fany]


def cache(
    expire_in: Optional[timedelta] = None,
    **kwargs: Any,
) -> Decorator:
    """
    Make function results cachable between calls.
    """

    def decorator(function: Fany) -> Fany:
        memo: Cache[Any, Any] = Cache(**kwargs)

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, kwargs)
            try:
                return memo.get(key)
            except KeyError:
                pass  # item not in cache, lets add it and return

            result = function(*args, **kwargs)
            memo.save(key, result, expire_in=expire_in)
            return result

        return wrapper

    return decorator
