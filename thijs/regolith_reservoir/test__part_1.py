from os import path
from typing import Iterable

from pytest import fixture

from .part_1 import CaveSystem, Segment, read_rock_segments


@fixture
def sample_data():
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return read_rock_segments(INPUT_PATH)
# END sample_data


@fixture
def data():
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return read_rock_segments(INPUT_PATH)
# END data


def test__init_rock_map(sample_data: Iterable[Segment]):

    expected_outcome = {(496, 6), (497, 6), (498, 6), (498, 5), (498, 4), (494, 9), (495, 9), (496, 9), (497, 9), (
        498, 9), (499, 9), (500, 9), (501, 9), (502, 9), (502, 8), (502, 7), (502, 6), (502, 5), (502, 4), (503, 4)}

    cave_system = CaveSystem()

    cave_system.init_rock_map(sample_data)

    assert cave_system.rock_map == expected_outcome
# END test__init_rock_map


def test__simulate_sand_from_sample(sample_data: Iterable[Segment]):
    cave_system = CaveSystem()

    cave_system.init_rock_map(sample_data)

    cave_system.simulate_sand()

    assert len(cave_system.sand_map) == 24
# END test__simulate_sand_from_sample


def test__simulate_sand(data: Iterable[Segment]):
    cave_system = CaveSystem()

    cave_system.init_rock_map(data)

    cave_system.simulate_sand()

    assert len(cave_system.sand_map) == 795
# END test__simulate_sand
