from os import path

from pytest import fixture

from .part_1 import (JetPattern, has_collision, merge, read_jet_pattern,
                     shift_left, shift_right, simulate_falling_rocks)


@fixture
def sample_data() -> JetPattern:
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return read_jet_pattern(INPUT_PATH)
# END sample_data


@fixture
def data() -> JetPattern:
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return read_jet_pattern(INPUT_PATH)
# END data


def test__shift_left():
    assert shift_left([[0, 0, 1, 1, 1, 1, 0]]) == [[0, 1, 1, 1, 1, 0, 0]]
# END test__shift_left


def test__shift_left_blocked():
    assert shift_left([[1, 1, 1, 1, 0, 0, 0]]) == [[1, 1, 1, 1, 0, 0, 0]]
# END test__shift_left


def test__shift_right():
    assert shift_right([[0, 0, 1, 1, 1, 1, 0]]) == [[0, 0, 0, 1, 1, 1, 1]]
# END test__shift_left


def test__shift_right_blocked():
    assert shift_right([[0, 0, 0, 1, 1, 1, 1]]) == [[0, 0, 0, 1, 1, 1, 1]]
# END test__shift_left


def test__has_collision_with_collision():
    assert has_collision([1, 1], [0, 1])
# END test__has_collision_with_collision


def test__has_collision_without_collision():
    assert not has_collision([1, 1], [0, 0])
# END test__has_collision_without_collision


def test__merge():
    assert merge([0, 1], [1, 0]) == [1, 1]
# END test__merge


def test__simulate_falling_rocks_sample_data(sample_data: JetPattern):
    tower = simulate_falling_rocks(3, sample_data)
    assert len(tower)  == 6
# END test__simulate_falling_rocks_sample_data
