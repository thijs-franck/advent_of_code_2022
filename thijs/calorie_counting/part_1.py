from collections import defaultdict
from os import path
from typing import Dict, List
from uuid import UUID
from uuid import uuid4 as uuid

CaloriesPerElf = Dict[UUID, List[int]]

INPUT_PATH = path.join(path.dirname(__file__), 'data')


def read_calories_per_elf(path: str) -> CaloriesPerElf:

    calories_per_elf: CaloriesPerElf = defaultdict(list)
    elf_id = uuid()

    with open(path) as file:
        for line in file:

            # An empty line indicates a new elf
            if line == '\n':
                elf_id = uuid()
                continue
            # END IF

            calories = int(line)
            calories_per_elf[elf_id].append(calories)
        # END LOOP
    # END WITH file

    return calories_per_elf
# END read_calories_per_elf


def find_largest_total_calories(calories_per_elf: CaloriesPerElf):
    total_calories_per_elf = map(sum, calories_per_elf.values())
    return max(total_calories_per_elf)
# END find_largest_total_calories


if __name__ == '__main__':
    calories_per_elf = read_calories_per_elf(INPUT_PATH)
    largest_total_calories = find_largest_total_calories(calories_per_elf)

    print(largest_total_calories)
# END MAIN
