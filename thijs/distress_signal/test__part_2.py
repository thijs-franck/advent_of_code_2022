from os import path
from typing import Iterable

from pytest import fixture

from .part_2 import Packet, read_packets


@fixture
def sample_data() -> Iterable[Packet]:
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return read_packets(INPUT_PATH)
# END sample_data


@fixture
def data() -> Iterable[Packet]:
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return read_packets(INPUT_PATH)
# END data

def test__part_2_sample(sample_data: Iterable[Packet]):

    divider_a = Packet([[2]])
    divider_b = Packet([[6]])

    sorted_packets = sorted([*sample_data, divider_a, divider_b])

    assert sorted_packets.index(divider_a) + 1 == 10
    assert sorted_packets.index(divider_b) + 1 == 14
# END test__part_2_sample


def test__part_2(data: Iterable[Packet]):

    divider_a = Packet([[2]])
    divider_b = Packet([[6]])

    sorted_packets = sorted([*data, divider_a, divider_b])

    assert (sorted_packets.index(divider_a) + 1) * (sorted_packets.index(divider_b) + 1) == 19493
# END test__part_2

