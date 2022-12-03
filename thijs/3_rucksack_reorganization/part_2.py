from itertools import islice
from os import path
from typing import Iterable, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), 'data')

RucksackItem = str
RucksackContent = Iterable[RucksackItem]
Group = Tuple[RucksackContent, RucksackContent, RucksackContent]


PRIORITY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_priority(items: Iterable[RucksackItem]) -> int:
    return sum(PRIORITY.index(item) + 1 for item in items)
# END get_priority


def read_groups(path: str, group_size: int) -> Iterable[Group]:
    with open(path) as file:
        rucksacks = (line.rstrip('\n') for line in file)
        while group := tuple(islice(rucksacks, group_size)):
            yield group
        # END LOOP
    # END WITH file
# END read_groups


def get_common_items(group: Group) -> Set[RucksackItem]:
    first, *others = group
    return set(first).intersection(*others)
# END get_common_items


def get_total_priority(groups: Iterable[Group]) -> int:
    common_items = map(get_common_items, groups)
    return sum(get_priority(items) for items in common_items)
# END get_total_priority


if __name__ == '__main__':
    groups = read_groups(INPUT_PATH, 3)
    total_priority = get_total_priority(groups)

    print(total_priority)
# END MAIN
