from typing import Any
import pytest

from mycache import Map


def test_map_constructors() -> None:
    pycaches_map: Map[str, int] = Map()
    assert len(pycaches_map) == 0

    pycaches_map = Map({"1": 1})
    assert pycaches_map["1"] == 1

    pycaches_map = Map([("2", 2)])
    assert pycaches_map["2"] == 2


def test_map_to_dictionary() -> None:
    python_dict = {"1": 1, "2": 2, "3": 3}
    pycaches_map = Map(python_dict)

    assert dict(pycaches_map) == python_dict


def test_map_in_operator() -> None:
    pycaches_map = Map({"1": 1, "2": 2, "3": 3})

    assert "1" in pycaches_map
    assert "2" in pycaches_map
    assert "3" in pycaches_map
    assert "4" not in pycaches_map
    assert None not in pycaches_map


def test_map_getitem() -> None:
    pycaches_map = Map({"1": 1, "2": 2, "3": 3})

    assert pycaches_map["1"] == 1
    assert pycaches_map["2"] == 2
    assert pycaches_map["3"] == 3

    with pytest.raises(KeyError):
        _ = pycaches_map["4"]


def test_map_len() -> None:
    pycaches_map = Map({"1": 1, "2": 2, "3": 3})
    assert len(pycaches_map) == 3

    pycaches_map["4"] = 4
    assert len(pycaches_map) == 4

    pycaches_map["1"] = 11
    assert len(pycaches_map) == 4


def test_map_setitem() -> None:
    pycaches_map = Map({"1": 1, "2": 2, "3": 3})
    pycaches_map["1"] = 11
    pycaches_map["4"] = 4

    assert pycaches_map["1"] == 11
    assert pycaches_map["4"] == 4


def test_map_delitem() -> None:
    pycaches_map = Map({"1": 1, "2": 2, "3": 3})
    del pycaches_map["1"]

    assert "1" not in pycaches_map


def test_unhashable_items_in_maps() -> None:
    pycaches_map: Map[Any, str] = Map()
    examples = [
        (["key"], "list value"),
        ({"key": "key"}, "dict value"),
        ({"key"}, "set value"),
    ]

    for key, value in examples:
        pycaches_map[key] = value
        assert pycaches_map[key] == value
        assert key in pycaches_map

    assert len(pycaches_map) == len(examples)

    pycaches_map[examples[0][0]] = "any value"
    assert len(pycaches_map) == len(examples)


def test_unhashable_items_deletion() -> None:
    pycaches_map: Map[Any, str] = Map()
    examples = [
        (["key"], "list value"),
        ({"key": "key"}, "dict value"),
        ({"key"}, "set value"),
    ]
    for key, value in examples:
        pycaches_map[key] = value

    for key, _ in examples:
        del pycaches_map[key]
        assert key not in pycaches_map


def test_unhashable_items_raises_errors() -> None:
    pycaches_map: Map[Any, str] = Map()
    pycaches_map[1] = "1"
    pycaches_map[[2]] = "2"

    with pytest.raises(KeyError):
        _ = pycaches_map[["not existed value"]]

    with pytest.raises(KeyError):
        del pycaches_map[["not existed value"]]


def test_map_keys_values_items() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    assert list(pycaches_map.keys()) == ["1", {"2"}]
    assert list(pycaches_map.values()) == [1, 2]
    assert list(pycaches_map.items()) == [("1", 1), ({"2"}, 2)]


def test_map_get() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    assert pycaches_map.get({"2"}) == 2
    assert pycaches_map.get({"3"}) is None
    assert pycaches_map.get({"4"}, 4) == 4


def test_map_setdefault() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    pycaches_map.setdefault({"3"}, 3)
    assert pycaches_map.get({"3"}) == 3


def test_map_pop() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    assert len(pycaches_map) == 2
    assert pycaches_map.pop({"2"}) == 2
    assert len(pycaches_map) == 1


def test_map_update() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    pycaches_map.update([
        ("1", 11),
        ({"2"}, 22),
    ])
    assert pycaches_map["1"] == 11
    assert pycaches_map[{"2"}] == 22


def test_map_clear() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    pycaches_map.clear()
    assert len(pycaches_map) == 0


def test_map_copy() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1})
    pycaches_map[{"2"}] = 2

    newmap = pycaches_map.copy()
    assert newmap == pycaches_map
    assert id(newmap) != id(pycaches_map)


def test_map_equality() -> None:
    assert Map({"1": 1, "2": 2}) == Map({"2": 2, "1": 1})
    assert Map({"1": 1, "2": 2}) != Map({"2": 2})
    assert Map({"1": 1, "2": 2}) != Map({"3": 3, "2": 2, "1": 1})

    assert Map({"1": 1, "2": 2}) != [1, 2]
    assert Map({"1": 1, "2": 2}) != {"1": 1, "2": 2}


def test_map_iterable() -> None:
    pycaches_map: Map[Any, int] = Map({"1": 1, "2": 2, "3": 3})
    pycaches_map[{4: 4}] = 4

    keys = [key for key in pycaches_map]  # pylint: disable=R1721
    assert keys == ["1", "2", "3", {4: 4}]


def test_map_uses_deepcopy_by_default() -> None:
    pycaches_map: Map[Any, int] = Map()
    key = {"some": "key"}

    pycaches_map[key] = 1
    assert key in pycaches_map

    key["another"] = "value"
    assert key not in pycaches_map


def test_map_allows_to_disable_deepcopy() -> None:
    pycaches_map: Map[Any, int] = Map(copy_keys=False)
    key = {"some": "key"}

    pycaches_map[key] = 1
    assert key in pycaches_map

    key["another"] = "value"
    assert key in pycaches_map
    assert {"some": "key"} not in pycaches_map


def test_map_saves_nested_unhashables() -> None:
    pycaches_map: Map[Any, str] = Map()
    key = ({1}, {2})
    value = "whatever"

    pycaches_map[key] = value
    assert pycaches_map[key] == value
