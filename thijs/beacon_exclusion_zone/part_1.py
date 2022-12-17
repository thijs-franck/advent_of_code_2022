import re
from os import path
from typing import Iterable, Optional, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Point = Tuple[int, int]
Range = Tuple[int, int]
Segment = Range

Beacon = Point
Sensor = Point


def manhattan_distance(a: Point, b: Point) -> int:
    """
    Calculates the manhattan distance between the given points `a` and `b`.
    """

    x_a, y_a = a
    x_b, y_b = b

    return abs(x_a - x_b) + abs(y_a - y_b)
# END manhattan_distance


def read_sensors_and_beacons(path: str) -> Iterable[Tuple[Sensor, Beacon]]:
    """
    Reads the input data at the given `path` and yields the position of each `Sensor` and its closest `Beacon`.
    """

    PATTERN = r"Sensor at x=(?P<sensor_x>\d+), y=(?P<sensor_y>\d+): closest beacon is at x=(?P<beacon_x>\d+), y=(?P<beacon_y>\d+)"

    with open(path) as file:

        lines = (line.rstrip("\n") for line in file)

        for line in lines:
            matches = re.match(
                pattern=PATTERN,
                string=line
            )

            if matches is None:
                continue
            # END IF

            sensor_x, sensor_y, beacon_x, beacon_y = matches.groupdict().values()

            yield (int(sensor_x), int(sensor_y)), (int(beacon_x), int(beacon_y))
        # END LOOP
    # END WITH file
# END read_sensors_and_beacons


def calculate_exclusion_range(sensor: Sensor, beacon: Beacon, y: int) -> Optional[Range]:
    """
    Given a `sensor` and its closest `beacon`, calculates the range on axis `y` where no other beacons can exist.
    Returns `None` if no points on axis `y` are excluded.
    """

    sensor_x, sensor_y = sensor

    distance = manhattan_distance(sensor, beacon)

    range = distance - abs(sensor_y - y)

    if range < 0:
        return None
    # END IF

    return (sensor_x - range, sensor_x + range)
# END points_in_range


def are_disjoint(a: Range, b: Range) -> bool:
    """
    Returns `True` if ranges `a` and `b` do not overlap or touch at either ends.
    """

    a_start, a_end = a
    b_start, b_end = b

    return a_start - b_end > 1 or b_start - a_end > 1
# END are_disjoint


def calculate_segments(ranges: Iterable[Range]) -> Set[Segment]:
    """
    Merges the given ranges into segments.
    """

    segments: Set[Segment] = set()

    for range in ranges:
        range_start, range_end = range
        new_segments = segments.copy()

        for segment in segments:
            segment_start, segment_end = segment

            if not are_disjoint((range_start, range_end), segment):
                new_segments.discard(segment)
                range_start = min(segment_start, range_start)
                range_end = max(segment_end, range_end)
            # END IF
        else:
            new_segments.add((range_start, range_end))
        # END LOOP

        segments = new_segments
    # END LOOP

    return segments
# END calculate_segments


def count_blocked_positions(segments: Iterable[Segment]) -> int:
    """
    Returns the sum of the length of all given `segments`.
    A segment has a minimum length of `1`.
    """
    
    return sum(1 + end - start for start, end in segments)
# END count_blocked_positions


if __name__ == "__main__":
    sensors_and_beacons = list(read_sensors_and_beacons(INPUT_PATH))

    _, beacons = zip(*sensors_and_beacons)

    beacons_in_line = set(x for x, y in beacons if y == 2000000)

    ranges = filter(None, (
        calculate_exclusion_range(sensor, beacon, 2000000)
        for sensor, beacon
        in sensors_and_beacons
    ))

    segments = calculate_segments(ranges)

    blocked_positions = count_blocked_positions(segments)

    print(blocked_positions - len(beacons_in_line))
# END MAIN
