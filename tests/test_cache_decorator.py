from unittest.mock import Mock

from mycache import cache


def test_it_prevents_function_calls() -> None:
    function = Mock()
    wrapped_function = cache()(function)

    assert function.call_count == 0

    wrapped_function()
    assert function.call_count == 1

    wrapped_function()
    assert function.call_count == 1

    wrapped_function("x", "y")
    assert function.call_count == 2

    wrapped_function("x", "y")
    assert function.call_count == 2

    wrapped_function(x="x", y="y")
    assert function.call_count == 3

    wrapped_function(y="y", x="x")
    assert function.call_count == 3
