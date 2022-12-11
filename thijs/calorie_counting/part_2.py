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


def find_total_calories_for_top_elves(calories_per_elf: CaloriesPerElf, top_n: int):
    total_calories_per_elf = map(sum, calories_per_elf.values())
    sorted_calories_per_elf = sorted(total_calories_per_elf)
    top_n_calories_per_elf = sorted_calories_per_elf[-top_n:]
    return sum(top_n_calories_per_elf)
# END find_total_calories_for_top_elves


if __name__ == '__main__':
    calories_per_elf = read_calories_per_elf(INPUT_PATH)

    total_calories_for_top_elves = find_total_calories_for_top_elves(
        calories_per_elf,
        top_n=3
    )

    print(total_calories_for_top_elves)
# END MAIN
