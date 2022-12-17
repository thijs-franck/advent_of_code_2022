from os import path
from typing import List, Tuple

from pytest import fixture

from .part_1 import (Beacon, Sensor, are_disjoint, calculate_segments,
                     count_blocked_positions, points_in_range,
                     read_sensors_and_beacons)


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


def test__points_in_range():
    range = points_in_range((8, 7), (2, 10), 10)
    assert range == (2, 14)

    range = points_in_range((9, 16), (10, 16), 17)
    assert range == (9, 9)

    range = points_in_range((2, 18), (-2, 15), 15)
    assert range == (-2, 6)

    range = points_in_range((4, 9), (4, 5), 12)
    assert range == (3, 5)
# END test__points_in_range


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


def test__count_blocked_positions_sample_data_9(sample_data: List[Tuple[Sensor, Beacon]]):

    _, beacons = zip(*sample_data)

    beacons_in_line = set(x for x, y in beacons if y == 9)

    ranges = list(filter(None, (
        points_in_range(sensor, beacon, 9)
        for sensor, beacon
        in sample_data
    )))

    segments = calculate_segments(ranges)

    blocked_positions = count_blocked_positions(segments)

    assert blocked_positions - len(beacons_in_line) == 25
# END test__count_blocked_positions_sample_data_9


def test__count_blocked_positions_sample_data_10(sample_data: List[Tuple[Sensor, Beacon]]):

    _, beacons = zip(*sample_data)

    beacons_in_line = set(x for x, y in beacons if y == 10)

    ranges = list(filter(None, (
        points_in_range(sensor, beacon, 10)
        for sensor, beacon
        in sample_data
    )))

    segments = calculate_segments(ranges)

    blocked_positions = count_blocked_positions(segments)

    assert blocked_positions - len(beacons_in_line) == 26
# END test__count_blocked_positions_sample_data_10


def test__count_blocked_positions_sample_data_11(sample_data: List[Tuple[Sensor, Beacon]]):

    _, beacons = zip(*sample_data)

    beacons_in_line = set(x for x, y in beacons if y == 11)

    ranges = list(filter(None, (
        points_in_range(sensor, beacon, 11)
        for sensor, beacon
        in sample_data
    )))

    segments = calculate_segments(ranges)

    blocked_positions = count_blocked_positions(segments)

    assert blocked_positions - len(beacons_in_line) == 28
# END test__count_blocked_positions_sample_data_11


def test__count_blocked_positions(data: List[Tuple[Sensor, Beacon]]):

    _, beacons = zip(*data)

    beacons_in_line = set(x for x, y in beacons if y == 2000000)

    ranges = list(filter(None, (
        points_in_range(sensor, beacon, 2000000)
        for sensor, beacon
        in data
    )))

    segments = calculate_segments(ranges)

    blocked_positions = count_blocked_positions(segments)

    assert blocked_positions - len(beacons_in_line) == 26
# END test__count_blocked_position
