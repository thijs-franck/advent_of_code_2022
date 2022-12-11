from os import path
from typing import Iterable, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), 'data')

RucksackItem = str
RucksackCompartment = Iterable[RucksackItem]
Rucksack = Tuple[RucksackCompartment, RucksackCompartment]


PRIORITY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_priority(items: Iterable[RucksackItem]) -> int:
    return sum(PRIORITY.index(item) + 1 for item in items)
# END get_priority


def read_rucksacks(path: str) -> Iterable[Rucksack]:
    with open(path) as file:
        rucksacks = (line.rstrip('\n') for line in file)
        for rucksack in rucksacks:
            split_index = len(rucksack)//2
            yield rucksack[:split_index], rucksack[split_index:]
        # END LOOP
    # END WITH file
# END read_rucksacks


def get_common_items(rucksack: Rucksack) -> Set[RucksackItem]:
    left, right = rucksack
    return set(left).intersection(right)
# END get_common_items


def get_total_priority(rucksacks: Iterable[Rucksack]) -> int:
    common_items = map(get_common_items, rucksacks)
    return sum(get_priority(items) for items in common_items)
# END get_total_priority


if __name__ == '__main__':
    rucksacks = read_rucksacks(INPUT_PATH)
    total_priority = get_total_priority(rucksacks)

    print(total_priority)
# END MAIN
