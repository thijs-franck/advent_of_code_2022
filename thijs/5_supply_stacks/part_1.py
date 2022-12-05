import re
from collections import deque
from dataclasses import dataclass
from os import path
from typing import Deque, Iterable, List

STACKS_PATH = path.join(path.dirname(__file__), "crates")
MOVES_PATH = path.join(path.dirname(__file__), "moves")

Stacks = List[Deque[str]]


@dataclass
class MoveParseException(Exception):
    input_string: str
# END MoveParseException


@dataclass
class Move:
    quantity: int
    source: int
    target: int

    @classmethod
    def from_input_string(cls, input_string: str):
        matches = re.match(
            pattern=r'move (?P<quantity>\d+) from (?P<source>\d+) to (?P<target>\d+)',
            string=input_string
        )

        if matches is None:
            raise MoveParseException(input_string)
        # END IF

        arguments = {key: int(value)
                     for key, value in matches.groupdict().items()}

        return cls(**arguments)
    # END from_input_string

# END Move


def read_moves(path: str) -> Iterable[Move]:
    with open(path) as file:
        moves = (line.rstrip('\n') for line in file)
        for move in moves:
            yield Move.from_input_string(move)
        # END LOOP
    # END WITH file
# END read_moves


def read_stacks(path: str) -> Stacks:
    stacks: Stacks = [deque() for _ in range(0, 9)]

    with open(path) as file:
        levels = (line.rstrip('\n') for line in file)
        for level in levels:
            for index, stack in enumerate(stacks):
                crate = level[index * 4 + 1]

                if crate == " ":
                    continue
                # END IF

                stack.appendleft(crate)
            # END LOOP
        # END LOOP
    # END WITH file
    return stacks
# END read_stacks


def apply_moves(stacks: Stacks, moves: Iterable[Move]) -> Stacks:
    for move in moves:
        source = stacks[move.source - 1]
        target = stacks[move.target - 1]

        crates = [source.pop() for _ in range(0, move.quantity)]

        for crate in crates:
            target.append(crate)
        # END LOOP
    # END LOOP
    return stacks
# END apply_moves


if __name__ == '__main__':
    moves = read_moves(MOVES_PATH)
    stacks = read_stacks(STACKS_PATH)

    apply_moves(stacks, moves)

    print("".join([stack[-1] for stack in stacks]))
# END IF
