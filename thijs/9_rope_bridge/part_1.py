from os import path
from typing import Callable, Dict, Iterable, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Direction = str
Distance = int
Move = Tuple[Direction, Distance]
Position = Tuple[int, int]
Movement = Callable[[Distance], Position]


def read_moves(path: str) -> Iterable[Move]:
    with open(path) as file:
        moves = (line.rstrip("\n") for line in file)
        for move in moves:
            direction, distance = move.split()
            yield (direction, int(distance))
        # END LOOP
    # END WITH file
# END read_moves


def track_bridge(moves: Iterable[Move]):

    head: Position = (0, 0)
    tail: Position = (0, 0)

    visited: Set[Position] = set()
    visited.add(tail)

    def ends_are_touching():
        return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1
    # END ends_are_touching

    movements: Dict[Direction, Movement] = {
        "U": lambda distance: (head[0], head[1] + distance),
        "D": lambda distance: (head[0], head[1] - distance),
        "R": lambda distance: (head[0] + distance, head[1]),
        "L": lambda distance: (head[0] - distance, head[1])
    }

    for direction, distance in moves:
        head = movements[direction](distance)

        while not ends_are_touching():
            dx = (
                max(-1, head[0] - tail[0])
                if tail[0] > head[0]
                else min(1, head[0] - tail[0])
            )

            dy = (
                max(-1, head[1] - tail[1])
                if tail[1] > head[1]
                else min(1, head[1] - tail[1])
            )

            tail = (tail[0] + dx, tail[1] + dy)

            visited.add(tail)
        # END LOOP
    # END LOOP

    return visited
# END track_bridge


if __name__ == "__main__":
    moves = read_moves(INPUT_PATH)
    visited = track_bridge(moves)

    print(len(visited))
# END MAIN
