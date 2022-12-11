from math import prod
from os import path
from typing import List

from part_1 import ClockCircuit, Instruction, read_instructions
from pytest import fixture


@fixture
def instructions_simple() -> List[Instruction]:
    return [("noop", None), ("addx", 3), ("addx", -5)]
# END instructions_simple

@fixture
def instructions_complex() -> List[Instruction]:
    PATH = path.join(path.dirname(__file__), "instructions_complex")
    return list(read_instructions(PATH))
# END instructions_complex


def test__clock_circuit_simple(instructions_simple: List[Instruction]):
    clock_circuit = ClockCircuit(instructions_simple)

    signals = [x for x in clock_circuit]

    assert signals == [(1, 1), (2, 1), (3, 1), (4, 4), (5, 4)]
    assert clock_circuit.x == -1
# END test__clock_cirquit_simple


def test__clock_circuit_complex(instructions_complex: List[Instruction]):
    clock_circuit = ClockCircuit(instructions_complex)

    signals = [x for x in clock_circuit]

    signal_strength = [prod(signals[cycle]) for cycle in range(19, len(signals), 40)]

    assert signal_strength == [420, 1140, 1800, 2940, 2880, 3960]
# END test_clock_cirquit_complex