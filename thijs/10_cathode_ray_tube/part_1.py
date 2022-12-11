from dataclasses import dataclass
from math import prod
from os import path
from typing import Iterable, Optional, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Command = str
Arg = Optional[int]
Instruction = Tuple[Command, Arg]


def read_instructions(path: str) -> Iterable[Instruction]:
    with open(path) as file:
        instructions = (line.rstrip("\n") for line in file)
        for instruction in instructions:
            tokens = instruction.split()
            if tokens[0] == 'noop':
                yield (tokens[0], None)
            elif tokens[0] == 'addx':
                yield (tokens[0], int(tokens[1]))
            # END IF
        # END LOOP
    # END with
# END read_instructions


cycle_cost = {
    "noop": 1,
    "addx": 2
}


@dataclass
class ClockCircuit:

    instructions: Iterable[Instruction]

    ticks: int = 0
    x: int = 1

    current_instruction: Optional[Instruction] = None
    cycles_remaining: int = 0

    def addx(self, v: int):
        self.x += v
    # END addx

    def noop(self):
        pass
    # END noop

    def __iter__(self):        
        for instruction in self.instructions:
            command, arg = instruction

            self.current_instruction = instruction
            self.cycles_remaining = cycle_cost[command]

            while self.cycles_remaining > 0:
                self.ticks += 1

                yield (self.ticks, self.x)

                self.cycles_remaining -= 1

                if self.cycles_remaining == 0:
                    if command == "addx":
                        self.addx(arg)
                    elif command == "noop":
                        self.noop()
                    # END IF
                # END IF
            # END LOOP
        # END LOOP
    # END __iter__
# END ClockCircuit


if __name__ == "__main__":
    instructions = read_instructions(INPUT_PATH)

    clock_circuit = ClockCircuit(instructions)

    signal = [x for x in clock_circuit]
    signal_strength = [prod(signal[cycle]) for cycle in range(19, len(signal), 40)]

    print(sum(signal_strength))
# END MAIN
