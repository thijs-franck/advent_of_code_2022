from os import path
from typing import List, Tuple

from pytest import fixture

from .part_1 import (read_valves, TunnelSystem, find_max_pressure_release, Valve)


@fixture
def sample_data() -> List[Valve]:
    INPUT_PATH = path.join(path.dirname(__file__), "sample_data")
    return list(read_valves(INPUT_PATH))
# END sample_data


@fixture
def data() -> List[Valve]:
    INPUT_PATH = path.join(path.dirname(__file__), "data")
    return list(read_valves(INPUT_PATH))
# END data

def test__find_max_pressure_release_sample_data(sample_data: List[Valve]):

    tunnel_system = TunnelSystem.from_valves(sample_data)

    max_pressure_release = find_max_pressure_release(tunnel_system, "AA", 30)

    assert max_pressure_release == 1651
# END test__find_max_pressure_release_sample_data
