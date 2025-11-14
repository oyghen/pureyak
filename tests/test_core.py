from contextlib import AbstractContextManager, nullcontext

import pytest

from pureyak import core


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
