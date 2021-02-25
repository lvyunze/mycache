"""
Set of different cache replacement policies.
"""

import random
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Generic, List, TypeVar


Key = TypeVar("Key")


class Policy(Generic[Key]):
    """
    Base class (interface) for any replacement policy.
    """

    @abstractmethod
    def next_to_replace(self) -> Key:
        """
        Returns `Key` to be replaced next.
        """

    @abstractmethod
    def add(self, key: Key) -> None:
        """
        Method called when new item with `key` added.
        """

    @abstractmethod
    def remove(self, key: Key) -> None:
        """
        Method called when old item with `key` removed.
        Always called after `add` callback.
        """

    @abstractmethod
    def access(self, key: Key) -> None:
        """
        Method called when item was accessed
        (with `Cache.has` or `Cache.get` methods).
        May be called even on items those are not in the `Cache`.
        """


@dataclass
class Random(Policy[Key]):
    """
    Policy which will replace random items.
    """

    _keys: List[Key] = field(default_factory=list)

    def next_to_replace(self) -> Key:
        return random.choice(self._keys)

    def add(self, key: Key) -> None:
        self._keys.append(key)

    def remove(self, key: Key) -> None:
        self._keys.remove(key)

    def access(self, _key: Key) -> None:
        pass


@dataclass
class LRU(Policy[Key]):
    """
    "Least Recent Used" cache replacement policy.
    Element that was accessed last will be replaced.
    """

    _keys: List[Key] = field(default_factory=list)

    def next_to_replace(self) -> Key:
        # Return oldest key
        return self._keys[0]

    def add(self, key: Key) -> None:
        self._keys.append(key)

    def remove(self, key: Key) -> None:
        self._keys.remove(key)

    def access(self, key: Key) -> None:
        if key not in self._keys:
            return

        # Move key on top of queue
        self.remove(key)
        self.add(key)
