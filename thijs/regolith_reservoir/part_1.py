from dataclasses import dataclass, field
from itertools import tee
from os import path
from typing import Iterable, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Point = Tuple[int, int]
Segment = Tuple[Point, Point]


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
# END pairwise


def fmt_point(point: str) -> Point:
    x, y = point.split(",")
    return (int(x), int(y))
# END fmt_point


def read_rock_segments(path: str) -> Iterable[Segment]:
    with open(path) as file:
        rock_paths = (line.rstrip("\n") for line in file)
        for rock_path in rock_paths:
            yield from pairwise(
                fmt_point(point)
                for point in rock_path.split(" -> ")
            )
        # END LOOP
    # END WITH file
# END read_rock_segments


@dataclass
class CaveSystem:

    rock_map: Set[Point] = field(default_factory=set)

    sand_entrance: Point = (500, 0)
    sand_map: Set[Point] = field(default_factory=set)

    def init_rock_map(self, segments: Iterable[Segment]):
        for a, b in segments:
            x_a, y_a = a
            x_b, y_b = b

            x_start = min(x_a, x_b)
            x_end = max(x_a, x_b)

            for x in range(x_start, x_end + 1):
                self.rock_map.add((x, y_a))
            # END LOOP

            y_start = min(y_a, y_b)
            y_end = max(y_a, y_b)

            for y in range(y_start, y_end + 1):
                self.rock_map.add((x_a, y))
            # END LOOP
        # END LOOP
    # END init_rock_map

    def simulate_sand(self):

        x, y = self.sand_entrance
        max_y = max(y for _, y in self.rock_map)

        while y < max_y:
            if not (
                (x, y + 1) in self.rock_map
                or (x, y + 1) in self.sand_map
            ):
                y += 1
                continue
            # END IF

            if not (
                (x - 1, y + 1) in self.rock_map
                or (x - 1, y + 1) in self.sand_map
            ):
                x -= 1
                y += 1
                continue
            # END IF

            if not (
                (x + 1, y + 1) in self.rock_map
                or (x + 1, y + 1) in self.sand_map
            ):
                x += 1
                y += 1
                continue
            # END IF

            self.sand_map.add((x, y))
            x, y = self.sand_entrance
        # END LOOP
    # END simulate_sand

# END CaveSystem

if __name__ == "__main__":

    cave_system = CaveSystem()
    rock_segments = read_rock_segments(INPUT_PATH)
    cave_system.init_rock_map(rock_segments)
    cave_system.simulate_sand()

    print(len(cave_system.sand_map))
# END MAIN