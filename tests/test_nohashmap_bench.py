import random
from typing import Any, Dict

from mycache import Map


def test_map_setitem_performance(benchmark: Any) -> None:
    pycaches_map: Map[Any, float] = Map()

    def insert_pycaches_map() -> None:
        value = random.random()

        for _ in range(100):
            key = random.randint(1, 75)
            pycaches_map[{"key": key}] = value

    benchmark(insert_pycaches_map)


def test_dict_setitem_performance(benchmark: Any) -> None:
    dict_map: Dict[Any, float] = dict()

    def insert_dict_map() -> None:
        value = random.random()

        for _ in range(100):
            key = random.randint(1, 75)
            dict_map[("key", key)] = value

    benchmark(insert_dict_map)


def test_empty_map_contains_performance(benchmark: Any) -> None:
    pycaches_map: Map[Any, int] = Map()

    def get_from_pycaches_map() -> None:
        key = random.randint(1, 75)
        _ = {"key": key} in pycaches_map

    benchmark(get_from_pycaches_map)


def test_empty_dict_contains_performance(benchmark: Any) -> None:
    dict_map: Dict[Any, int] = dict()

    def get_from_dict_map() -> None:
        key = random.randint(1, 75)
        _ = ("key", key) in dict_map

    benchmark(get_from_dict_map)
