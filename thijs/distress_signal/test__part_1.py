from os import path
from typing import Iterable

from pytest import fixture

from .part_1 import Pair, is_ordered, read_pairs


@fixture
def sample_data() -> Iterable[Pair]:
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return read_pairs(INPUT_PATH)
# END sample_data


@fixture
def data() -> Iterable[Pair]:
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return read_pairs(INPUT_PATH)
# END data


def test__is_ordered(sample_data: Iterable[Pair]):
    ordered = [is_ordered(pair.left, pair.right) for pair in sample_data]

    assert ordered == [True, True, False, True, False, True, False, False]
# END test__is_ordered


def test__part_1_sample(sample_data: Iterable[Pair]):
    result = sum(
        pair.index
        for pair in sample_data
        if is_ordered(pair.left, pair.right)
    )

    assert result == 13
# END test__part_1_sample


def test__part_1(data: Iterable[Pair]):
    result = sum(
        pair.index
        for pair in data
        if is_ordered(pair.left, pair.right)
    )

    assert result == 6568
# END test__part_1
