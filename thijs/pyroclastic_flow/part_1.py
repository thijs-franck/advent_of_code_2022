from typing import List

Vertex = List[int]
Shape = List[Vertex]
JetPattern = str

HORIZONRAL: Shape = [
    [0, 0, 1, 1, 1, 1, 0]
]

PLUS: Shape = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0]
]

CORNER: Shape = [
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0]
]

VERTICAL: Shape = [
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0]
]

BLOCK: Shape = [
    [0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0]
]

ROCKS: List[Shape] = [HORIZONRAL, PLUS, CORNER, VERTICAL, BLOCK]


def shift_left(shape: Shape) -> Shape:

    if any(row[0] for row in shape):
        return shape
    # END IF

    return [[row[(index + 1) % len(row)] for index in range(len(row))] for row in shape]
# END shift_left


def shift_right(shape: Shape) -> Shape:

    if any(row[-1] for row in shape):
        return shape
    # END IF

    return [[row[(index - 1) % len(row)] for index in range(len(row))] for row in shape]
# END shift_right


def has_collision(a: Vertex, b: Vertex) -> bool:
    return any(i and j for i, j in zip(a, b))
# END has_collision


def merge(a: Vertex, b: Vertex) -> Vertex:
    return [max(i, j) for i, j in zip(a, b)]
# END merge


MOVEMENTS = {
    ">": shift_right,
    "<": shift_left
}


def read_jet_pattern(path: str) -> JetPattern:
    with open(path) as file:
        return file.read()
    # END WITH file
# END read_jet_pattern


def simulate_falling_rocks(n_rocks: int, jet_pattern: JetPattern) -> Shape:

    tower: Shape = [[1, 1, 1, 1, 1, 1, 1]]
    ticks = 0

    for i in range(n_rocks):

        base_y = len(tower) + 3
        shape = ROCKS[i % len(ROCKS)]
        dy = 0

        while not any(
            has_collision(vertex, tower[base_y - dy + index])
            for index, vertex
            in enumerate(reversed(shape))
            if 0 <= base_y - dy + index < len(tower)
        ):
            direction = jet_pattern[ticks % len(jet_pattern)]
            movement = MOVEMENTS[direction]
            shape = movement(shape)

            ticks += 1
            dy += 1
        # END LOOP

        for index, vertex in enumerate(reversed(shape)):
            y = base_y - (dy - 1) + index

            if y < len(tower):
                tower[y] = merge(vertex, tower[y])
            else:
                tower.append(vertex)
            # END LOOP
        # END LOOP
    # END LOOP

    return tower
# END simulate_falling_rocks
