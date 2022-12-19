from os import path
from typing import List

from pytest import fixture

from .part_2 import TunnelSystem, Valve, find_max_pressure_release, read_valves


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

    max_pressure_release = find_max_pressure_release(
        tunnel_system,
        "AA",
        2,
        26
    )

    assert max_pressure_release == 1707
# END test__find_max_pressure_release_sample_data


def test__find_max_pressure_release(data: List[Valve]):

    tunnel_system = TunnelSystem.from_valves(data)

    max_pressure_release = find_max_pressure_release(tunnel_system, "AA", 30)

    assert max_pressure_release == 2253
# END test__find_max_pressure_release_sample_data
