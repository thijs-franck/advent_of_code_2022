import json
from dataclasses import dataclass
from itertools import zip_longest
from os import path
from typing import Iterable, List, Tuple, TypeVar, Union, Optional

INPUT_PATH = path.join(path.dirname(__file__), "data")


Packet = List[Union[int, 'Packet']]

T = TypeVar('T')


def grouper(n: int, iterable: Iterable[T], fillvalue: T = None) -> Iterable[Tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)
# END grouper


def is_ordered(left: Packet, right: Packet) -> Optional[bool]:
    for(a, b) in zip(left, right):
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return True
            elif a > b:
                return False
            else:
                continue
            # END IF
        # END IF

        if isinstance(a, int):
            a = [a]
        # END IF

        if isinstance(b, int):
            b = [b]
        # END IF

        result = is_ordered(a, b)

        if result is not None:
            return result
        # END IF
    # END LOOP

    if len(left) != len(right):
        return len(left) < len(right)
    # END IF

    return None
# END is_ordered


@dataclass
class Pair:
    index: int
    left: Packet
    right: Packet
# END Pair


def read_pairs(path: str) -> Iterable[Pair]:
    with open(path) as file:
        lines = (line.rstrip("\n") for line in file)
        packets = (json.loads(line) for line in lines if line != "")

        for index, (left, right) in enumerate(grouper(2, packets)):
            yield Pair(index=index + 1, left=left, right=right)
        # END LOOP
    # END WITH file
# END read_pairs


if __name__ == "__main__":
    pairs = read_pairs(INPUT_PATH)

    result = sum(
        pair.index 
        for pair in pairs 
        if is_ordered(pair.left, pair.right)
    )

    print(result)
# END MAIN
