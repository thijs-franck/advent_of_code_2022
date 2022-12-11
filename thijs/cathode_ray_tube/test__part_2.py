from os import path
from typing import List

from pytest import fixture

from .part_2 import ClockCircuit, Instruction, read_instructions, render_pixels


@fixture
def instructions_complex() -> List[Instruction]:
    PATH = path.join(path.dirname(__file__), "instructions_complex")
    return list(read_instructions(PATH))
# END instructions_complex


def test__render_pixels(instructions_complex: List[Instruction]):

    expected_output = "".join([
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ])

    clock_circuit = ClockCircuit(instructions_complex)

    rendered_output = render_pixels(clock_circuit, 40)

    assert rendered_output == expected_output
# END test__render_pixels
