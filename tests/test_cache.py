from datetime import timedelta
from typing import Any

from freezegun import freeze_time  # type: ignore
import pytest

from mycache import Cache
from mycache.policies import LRU, Policy


def test_cache_saves_items() -> None:
    cache: Cache[Any, Any] = Cache()
    key, value = {"key"}, "value"

    assert not cache.has(key)
    with pytest.raises(KeyError):
        _ = cache.get(key)

    cache.save(key, value)

    assert cache.has(key)
    assert cache.get(key) == value


def test_cache_ignores_expired_items() -> None:
    cache: Cache[Any, Any] = Cache()
    key, value = {"key"}, "value"

    with freeze_time("2020-10-01 12:00:00"):
        cache.save(key, value, expire_in=timedelta(seconds=10))

    with freeze_time("2020-10-01 12:00:09"):
        assert cache.has(key)
        assert cache.get(key) == value

    with freeze_time("2020-10-01 12:00:10"):
        assert not cache.has(key)

        with pytest.raises(KeyError):
            _ = cache.get(key)


def test_cache_remove_item() -> None:
    cache: Cache[Any, Any] = Cache()
    key, value = {"key"}, "value"

    cache.save(key, value)
    assert cache.has(key)

    cache.remove(key)
    assert not cache.has(key)


def test_cache_keeps_size_lesser_than_max_items() -> None:
    cache: Cache[Any, Any] = Cache(max_items=3)

    cache.save("1", 1)
    cache.save("2", 2)
    cache.save("3", 3)
    assert cache.size() == 3

    cache.save("4", 4)
    assert cache.size() == 3


def test_cache_clears_expired_items_before_replacement() -> None:
    lru: Policy[Any] = LRU()
    cache: Cache[Any, Any] = Cache(max_items=4, replacement_policy=lru)

    with freeze_time("2020-10-01 12:00:00"):
        cache.save("1", 1)
        cache.save("2", 2, expire_in=timedelta(seconds=20))
        cache.save("3", 3, expire_in=timedelta(seconds=10))
        cache.save("4", 4, expire_in=timedelta(seconds=10))

    with freeze_time("2020-10-01 12:00:10"):
        cache.save("5", 5)
        cache.save("6", 6)

        assert cache.has("1")
        assert cache.has("2")
        assert cache.has("5")
        assert cache.has("6")

        assert not cache.has("3")
        assert not cache.has("4")


def test_lru_policy() -> None:
    lru: Policy[Any] = LRU()
    cache: Cache[Any, Any] = Cache(max_items=4, replacement_policy=lru)

    cache.save("1", 1)
    cache.save("2", 2)
    cache.save("3", 3)
    cache.save("4", 4)

    cache.save("5", 5)
    assert not cache.has("1")

    _ = cache.get("2")
    cache.save("6", 6)
    assert cache.has("2")
    assert not cache.has("3")


def test_disable_copy_keys_can_cause_bugs() -> None:
    copy_cache: Cache[Any, Any] = Cache()
    bugged_cache: Cache[Any, Any] = Cache(copy_keys=False)
    key = [1]
    value = "value"

    copy_cache.save(key, value)
    bugged_cache.save(key, value)
    key[0] = 2  # mutating the key

    assert bugged_cache.has(key)
    assert bugged_cache.has([2])
    assert not bugged_cache.has([1])

    assert not copy_cache.has(key)
    assert not copy_cache.has([2])
    assert copy_cache.has([1])
