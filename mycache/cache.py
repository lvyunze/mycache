"""
Dictionary-like collection
with restrictions on total size and storage time
and replacement of elements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Generic, Optional, TypeVar

from mycache.nohashmap import Map
from mycache.policies import Policy, Random as RandomPolicy


Key = TypeVar("Key")
Value = TypeVar("Value")


@dataclass
class CacheItem(Generic[Value]):
    """
    Cache item, containing value and metadata, such as:
    cache hits, last access time, expiration time, etc.
    """

    value: Value
    expire_at: Optional[datetime]

    def expired(self) -> bool:
        """
        Checks if item is expired.
        """

        if self.expire_at is None:
            return False

        return datetime.now() >= self.expire_at


@dataclass
class Cache(Generic[Key, Value]):
    """
    Dictionary-like collection
    with restrictions on total size and storage time
    and replacement of elements.
    """

    copy_keys: bool = True
    max_items: Optional[int] = None
    replacement_policy: Policy[Key] = field(default_factory=RandomPolicy)
    _map: Map[Key, CacheItem[Value]] = field(init=False)

    def __post_init__(self) -> None:
        self._map = Map(copy_keys=self.copy_keys)

    def has(self, key: Key) -> bool:
        """
        Checks if item with `key` is cached and not expired.
        """

        self.replacement_policy.access(key)
        return key in self._map and not self._map[key].expired()

    def get(self, key: Key) -> Value:
        """
        Returns cached item for `key`
        or raises `KeyError` if item is expired.
        """

        item = self._map[key]
        if item.expired():
            raise KeyError(key)

        self.replacement_policy.access(key)
        return item.value

    def size(self) -> int:
        """
        Returns count of items in cache.
        """

        return len(self._map)

    def full(self) -> bool:
        """
        Checks if cache is full.
        """

        if self.max_items is None:
            # Cache with no `max_items` parameter will never become full
            return False

        return self.size() >= self.max_items

    def save(
        self,
        key: Key,
        value: Value,
        expire_in: Optional[timedelta] = None,
    ) -> None:
        """
        Adds item to cache.
        Replaces item if cache size exceed `self._max_items`.
        """

        if self.full():
            self.__remove_expired_items()

        if self.full():
            key_to_remove = self.replacement_policy.next_to_replace()
            self.remove(key_to_remove)

        expire_at: Optional[datetime] = None
        if expire_in is not None:
            expire_at = datetime.now() + expire_in

        self.replacement_policy.add(key)
        self._map[key] = CacheItem(value, expire_at)

    def remove(self, key: Key) -> None:
        """
        Removes item with `key` from the cache.
        Raises `KeyError` if there are no such item.
        """

        self.replacement_policy.remove(key)
        del self._map[key]

    def __remove_expired_items(self) -> None:
        keys_to_remove = []

        for key, item in self._map.items():
            if item.expired():
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self.remove(key)
