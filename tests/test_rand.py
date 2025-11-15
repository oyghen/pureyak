import random
from contextlib import AbstractContextManager, nullcontext

import pytest

from pureyak import rand


class TestRandomDraw:
    @pytest.mark.parametrize(
        "replace, size, expected",
        [
            (True, 5, ["b", "a", "c", "c", "b"]),
            (False, 2, ["c", "a"]),
            (False, 3, ["c", "a", "b"]),
        ],
    )
    def test_basic_behavior(self, replace: bool, size: int, expected: list[str]):
        items = ["a", "b", "c"]
        actual = rand.draw(items, replace, size, seed=101)
        assert actual == expected

    @pytest.mark.parametrize("replace, size", [(False, 1), (True, 1)])
    def test_empty_items_returns_empty_list(self, replace: bool, size: int):
        actual = rand.draw([], replace, size)
        expected = []
        assert actual == expected

    @pytest.mark.parametrize("replace, size", [(False, 0), (True, 0)])
    def test_size_zero_returns_empty_list(self, replace: bool, size: int):
        items = [1, 2, 3]
        actual = rand.draw(items, replace, size)
        expected = []
        assert actual == expected

    @pytest.mark.parametrize("replace, size", [(False, -1), (True, -1)])
    def test_negative_size_raises_value_error(self, replace: bool, size: int):
        items = [1, 2, 3]
        with pytest.raises(ValueError):
            rand.draw(items, replace, size)

    def test_no_replacement_size_greater_than_num_items_raises(self):
        items = ["a", "b"]
        with pytest.raises(ValueError):
            rand.draw(items, replace=False, size=3)

    def test_draw_beyond_number_of_items(self):
        items = ["x", "y", "z"]
        actual = rand.draw(items, replace=True, size=5, seed=101)
        expected = ["y", "x", "z", "z", "y"]
        assert actual == expected


@pytest.mark.parametrize(
    "seed, ctx",
    [
        (None, nullcontext()),
        (0, nullcontext()),
        (random.Random(1), nullcontext()),
        ("invalid seed", pytest.raises(ValueError)),
        (3.0, pytest.raises(ValueError)),
    ],
    ids=["none", "int_zero", "Random_inst", "bad_string", "bad_float"],
)
def test_get_rng(seed: rand.Seed, ctx):
    with ctx:
        rng = rand.get_rng(seed)
        assert isinstance(rng, random.Random)


@pytest.mark.parametrize(
    "size, lower, upper, ctx",
    [
        (30, 0, 2, nullcontext()),
        (30, 0, 10, nullcontext()),
        (99, 1, 100, nullcontext()),
        (30, -2, 2, nullcontext()),
        (30, -10, -2, nullcontext()),
        (1, 5, 5, pytest.raises(ValueError, match=r"empty range for randrange")),
        (1, 100, 10, pytest.raises(ValueError, match=r"empty range for randrange")),
    ],
    ids=[
        "0-1 values only",
        "small_range",
        "large_range",
        "one_negative",
        "two_negative",
        "lower == upper -> zero randrange",
        "lower > upper -> negative randrange",
    ],
)
def test_integers(
    size: int,
    lower: int,
    upper: int,
    ctx: AbstractContextManager[None],
    request: pytest.FixtureRequest,
):
    with ctx:
        random_integers = tuple(rand.integers(size, lower, upper))
        test_id = request.node.callspec.id
        if test_id == "0-1 values only":
            assert set(random_integers) == {0, 1}
        assert len(random_integers) == size
        assert min(random_integers) >= lower
        assert min(random_integers) < upper


class TestRandomShuffle:
    def test_basic_behavior(self):
        items = [10, 20, 30]
        actual = rand.shuffle(items, seed=101)
        expected = [30, 10, 20]
        assert actual == expected
        assert actual is not items
        # ensure original list is not modified
        assert items == [10, 20, 30]

    def test_shuffle_empty_list(self):
        items = []
        actual = rand.shuffle(items, seed=101)
        expected = []
        assert actual == expected
        assert actual is not items

    def test_shuffle_single_element(self):
        items = [42]
        actual = rand.shuffle(items, seed=101)
        expected = [42]
        assert actual == expected
        assert actual is not items
        # ensure original list is not modified
        assert items == [42]

    def test_new_list_is_returned(self):
        items = [10, 20, 30]
        actual = rand.shuffle(items, seed=101)
        expected = [30, 10, 20]
        assert actual == expected
        assert actual is not items

        items.pop(-1)
        assert items == [10, 20]
        assert len(actual) == 3
        assert actual == expected
