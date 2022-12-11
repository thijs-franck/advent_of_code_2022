from os import path
from typing import Iterable, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), 'data')

Pair = Tuple[Set[int], Set[int]]


def read_pairs(path: str) -> Iterable[Pair]:

    with open(path) as file:
        pairs = (line.rstrip('\n') for line in file)

        for pair in pairs:

            a, b = pair.split(',')

            lower_a, upper_a = a.split('-')
            lower_b, upper_b = b.split('-')

            yield (
                set(range(int(lower_a), int(upper_a) + 1)),
                set(range(int(lower_b), int(upper_b) + 1))
            )
        # END LOOP
    # END WITH file
# END read_pairs


def sections_are_subset(pair: Pair) -> bool:
    a, b = pair
    return a.issubset(b) or b.issubset(a)
# END sections_are_subset


if __name__ == "__main__":
    pairs = read_pairs(INPUT_PATH)

    is_subset = [
        pair for pair in pairs
        if sections_are_subset(pair)
    ]

    print(len(is_subset))
# END MAIN
