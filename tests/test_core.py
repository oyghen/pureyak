from contextlib import AbstractContextManager, nullcontext
from typing import Any

import pytest

from pureyak import core


@pytest.mark.parametrize(
    "items, expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2, 3), [1, 2, 3]),
        (range(1, 7), [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
        ([[], [1, 2], [3, 4, 5], [6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], 3, (4, 5), (6,)], [1, 2, 3, 4, 5, 6]),
        ([[[1, 2]], [3], 4, [[[5]]], [[[[6]]]]], [1, 2, 3, 4, 5, 6]),
        ([1, [2, 3, 4], [[5, 6]]], [1, 2, 3, 4, 5, 6]),
        ([1, [2, 3, 4, 5], 6, []], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [3, 4, 5], 6], [1, 2, 3, 4, 5, 6]),
        (([[1, 2], [3, 4, 5], 6],), [1, 2, 3, 4, 5, 6]),
        ([iter([1, (2, 3)]), 4, [], iter([[[5]], 6])], [1, 2, 3, 4, 5, 6]),
        (
            [["one", 2], 3, [4, "five"], ["six"]],
            ["one", 2, 3, 4, "five", "six"],
        ),
        (map(lambda x: 2 * x, range(1, 7)), [2, 4, 6, 8, 10, 12]),
        ((2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (tuple(2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (list(2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (([-1], 0, range(1, 7)), [-1, 0, 1, 2, 3, 4, 5, 6]),
        (([-1], 0, map(lambda x: 2 * x, range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, (2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, tuple(2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, list(2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (filter(lambda x: x % 2 == 0, range(1, 7)), [2, 4, 6]),
        ((-1, filter(lambda x: x % 2 == 0, range(1, 7))), [-1, 2, 4, 6]),
        (([-1], filter(lambda x: x % 2 == 0, range(1, 7))), [-1, 2, 4, 6]),
    ],
)
def test_flatten(items: Any, expected: list[Any]):
    actual = list(core.flatten(items))
    assert actual == expected


@pytest.mark.parametrize(
    "num_bits, expected, ctx",
    [
        # valid cases
        (2, 1, nullcontext()),
        (3, 3, nullcontext()),
        (8, 127, nullcontext()),
        (16, 32_767, nullcontext()),
        (32, 2_147_483_647, nullcontext()),
        (64, 9_223_372_036_854_775_807, nullcontext()),
        # invalid cases
        (0, None, pytest.raises(ValueError)),
        (1, None, pytest.raises(ValueError)),
        (-5, None, pytest.raises(ValueError)),
        (3.5, None, pytest.raises(TypeError)),
    ],
)
def test_max_signed_value(
    num_bits: int,
    expected: int | None,
    ctx: AbstractContextManager[None],
):
    with ctx:
        actual = core.max_signed_value(num_bits)
        if expected is not None:
            assert actual == expected
