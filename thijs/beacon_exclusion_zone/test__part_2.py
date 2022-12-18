from os import path
from typing import List, Tuple

from pytest import fixture

from .part_2 import (Beacon, Sensor, are_disjoint, calculate_exclusion_range,
                     calculate_segments, calculate_tuning_frequency,
                     find_missing_beacon, read_sensors_and_beacons)


@fixture
def sample_data() -> List[Tuple[Sensor, Beacon]]:
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return list(read_sensors_and_beacons(INPUT_PATH))
# END sample_data


@fixture
def data() -> List[Tuple[Sensor, Beacon]]:
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return list(read_sensors_and_beacons(INPUT_PATH))
# END data


def test__calculate_exclusion_range():
    range = calculate_exclusion_range((8, 7), (2, 10), 10)
    assert range == (2, 14)

    range = calculate_exclusion_range((9, 16), (10, 16), 17)
    assert range == (9, 9)

    range = calculate_exclusion_range((2, 18), (-2, 15), 15)
    assert range == (-2, 6)

    range = calculate_exclusion_range((4, 9), (4, 5), 12)
    assert range == (3, 5)
# END test__calculate_exclusion_range


def test__are_disjoint():
    disjoint = are_disjoint((1, 1), (3, 3))
    assert disjoint

    disjoint = are_disjoint((1, 1), (2, 2))
    assert not disjoint

    disjoint = are_disjoint((1, 1), (1, 1))
    assert not disjoint

    disjoint = are_disjoint((1, 1), (0, 0))
    assert not disjoint

    disjoint = are_disjoint((1, 1), (-1, -1))
    assert disjoint
# END test__are_disjoint


def test__calculate_segments():
    # Segments adjacent
    range = calculate_segments([(2, 2), (3, 3), (1, 1)])
    assert range == {(1, 3)}

    range = calculate_segments([(1, 1), (3, 3), (2, 2)])
    assert range == {(1, 3)}

    # Segments overlap
    range = calculate_segments([(1, 2), (2, 3)])
    assert range == {(1, 3)}

    range = calculate_segments([(2, 3), (1, 2)])
    assert range == {(1, 3)}

    # Segment is subset of another
    range = calculate_segments([(1, 3), (2, 3)])
    assert range == {(1, 3)}

    range = calculate_segments([(2, 3), (1, 3)])
    assert range == {(1, 3)}

    # Segments disjoint
    range = calculate_segments([(1, 1), (3, 3)])
    assert range == {(1, 1), (3, 3)}

    range = calculate_segments([(3, 3), (1, 1)])
    assert range == {(1, 1), (3, 3)}
# END test__calculate_segments


def test__calculate_tuning_frequency_sample_data(sample_data: List[Tuple[Sensor, Beacon]]):

    beacon = find_missing_beacon(sample_data, 20)

    assert beacon == (14, 11)

    tuning_frequency = calculate_tuning_frequency(beacon)

    assert tuning_frequency == 56000011
# END test__count_blocked_positions_sample_data


def test__calculate_tuning_frequency(data: List[Tuple[Sensor, Beacon]]):

    beacon = find_missing_beacon(data, 4000000)

    assert beacon is not None

    tuning_frequency = calculate_tuning_frequency(beacon)

    assert tuning_frequency == 56000011
# END test__count_blocked_position
