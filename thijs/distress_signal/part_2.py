import json

from os import path
from typing import Iterable, Optional

INPUT_PATH = path.join(path.dirname(__file__), "data")


class Packet(list):
    def __lt__(self, b):
        return is_ordered(self, b)
    # END __lt__
# END Packet


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


def read_packets(path: str) -> Iterable[Packet]:
    with open(path) as file:
        lines = (line.rstrip("\n") for line in file)
        packets = (Packet(json.loads(line)) for line in lines if line != "")
        yield from packets
    # END WITH file
# END read_pairs


if __name__ == "__main__":
    packets = read_packets(INPUT_PATH)

    divider_a = Packet([[2]])
    divider_b = Packet([[6]])

    sorted_packets = sorted([*packets, divider_a, divider_b])

    print((sorted_packets.index(divider_a) + 1) * (sorted_packets.index(divider_b) + 1))
# END MAIN
