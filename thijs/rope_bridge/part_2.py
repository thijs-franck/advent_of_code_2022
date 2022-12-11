from os import path
from typing import Callable, Dict, Iterable, List, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Direction = str
Distance = int
Move = Tuple[Direction, Distance]
Position = Tuple[int, int]
Movement = Callable[[Position, Distance], Iterable[Position]]

movements: Dict[Direction, Movement] = {
    "U": lambda position, distance: [(position[0], position[1] + (i + 1)) for i in range(distance)],
    "D": lambda position, distance: [(position[0], position[1] - (i + 1)) for i in range(distance)],
    "R": lambda position, distance: [(position[0] + (i + 1), position[1]) for i in range(distance)],
    "L": lambda position, distance: [(position[0] - (i + 1), position[1]) for i in range(distance)]
}


def are_touching(a: Position, b: Position):
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1
# END are_touching


def read_moves(path: str) -> Iterable[Move]:
    with open(path) as file:
        moves = (line.rstrip("\n") for line in file)
        for move in moves:
            direction, distance = move.split()
            yield (direction, int(distance))
        # END LOOP
    # END WITH file
# END read_moves


def track_bridge(moves: Iterable[Move], n_knots: int = 2):

    head = (0, 0)
    knots: List[Position] = [(0, 0) for _ in range(n_knots - 1)]

    visited: Set[Position] = set()
    visited.add(knots[-1])

    for direction, distance in moves:

        steps = movements[direction](head, distance)

        for step in steps:

            head = step
            last = step

            for index, current in enumerate(knots):

                if are_touching(last, current):
                    last = current
                    continue
                # END IF

                while not are_touching(last, current):
                    dx = (
                        max(-1, last[0] - current[0])
                        if current[0] > last[0]
                        else min(1, last[0] - current[0])
                    )

                    dy = (
                        max(-1, last[1] - current[1])
                        if current[1] > last[1]
                        else min(1, last[1] - current[1])
                    )

                    new = (current[0] + dx, current[1] + dy)
                    knots[index] = new
                    last = new

                    if index == len(knots) - 1:
                        visited.add(last)
                    # END IF
                # END LOOP
            # END LOOP
        # END LOOP
    # END LOOP

    return visited
# END track_bridge


if __name__ == "__main__":
    moves = read_moves(INPUT_PATH)
    visited = track_bridge(moves, 10)

    print(len(visited))
# END MAIN
