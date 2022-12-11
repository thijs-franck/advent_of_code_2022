from collections import deque
from dataclasses import dataclass, field
from math import floor, prod
from typing import Callable, Deque, Iterable, List, Tuple

WorryLevel = int
Operation = Callable[[WorryLevel], WorryLevel]
Test = Callable[[WorryLevel], bool]
Partners = Tuple[int, int]
Throw = Tuple[int, WorryLevel]


@dataclass
class Monkey:
    operation: Operation
    test: Test
    partners: Partners

    inspections = 0
    items: Deque[WorryLevel] = field(default_factory=deque)

    def inspect(self, item: WorryLevel) -> WorryLevel:
        self.inspections += 1
        return self.operation(item)
    # END inspect

    def take_turn(self) -> Iterable[Throw]:
        while len(self.items) > 0:
            item = self.items.popleft()

            print(f"Monkey inspects an item with a worry level of {item}")

            inspected_item = self.inspect(item)

            print(
                f"Worry level increases by {inspected_item - item} to {inspected_item}")

            worry_level = floor(inspected_item / 3)

            print(
                f"Monkey gets bored with item. Worry level is divided by 3 to {worry_level}")

            passes_test = self.test(worry_level)

            print(f"Worry level test result: {passes_test}")

            partner = self.partners[0] if passes_test else self.partners[1]

            print(
                f"Item with worry level {worry_level} is thrown to monkey {partner}")

            yield (partner, worry_level)
        # END LOOP
    # END take_turn

    def catch_item(self, item: WorryLevel):
        self.items.append(item)
    # END catch_item
# END Monkey


@dataclass
class Game:
    monkeys: List[Monkey] = field(default_factory=list)
    round: int = 0
    turn: int = 0
    worry_level: WorryLevel = 0

    def play_round(self):
        self.round += 1

        print(f"Turn {self.round}:")

        for index, monkey in enumerate(self.monkeys):

            print(f"Monkey {index}:")

            self.turn += 1

            for partner, item in monkey.take_turn():
                self.monkeys[partner].catch_item(item)
            # END LOOP
        # END LOOP

        print(
            f"After round {self.round}, the monkeys are holding items with these worry levels:"
        )

        for index, monkey in enumerate(self.monkeys):
            print(f"Monkey {index}: {monkey.items}")
        # END LOOP
    # END play_round
# END Game


def calculate_monkey_business(game: Game) -> int:
    inspections = sorted(
        (monkey.inspections for monkey in game.monkeys),
        reverse=True
    )
    return prod(inspections[0:2])
# END calculate_monkey_business


if __name__ == "__main__":

    monkeys = [
        Monkey(
            items=deque([73, 77]),
            operation=lambda old: old * 5,
            test=lambda item: item % 11 == 0,
            partners=(6, 5)
        ),
        Monkey(
            items=deque([57, 88, 80]),
            operation=lambda old: old + 5,
            test=lambda item: item % 19 == 0,
            partners=(6, 0)
        ),
        Monkey(
            items=deque([61, 81, 84, 69, 77, 88]),
            operation=lambda old: old * 19,
            test=lambda item: item % 5 == 0,
            partners=(3, 1)
        ),
        Monkey(
            items=deque([78, 89, 71, 60, 81, 84, 87, 75]),
            operation=lambda old: old + 7,
            test=lambda item: item % 3 == 0,
            partners=(1, 0)
        ),
        Monkey(
            items=deque([60, 76, 90, 63, 86, 87, 89]),
            operation=lambda old: old + 2,
            test=lambda item: item % 13 == 0,
            partners=(2, 7)
        ),
        Monkey(
            items=deque([88]),
            operation=lambda old: old + 1,
            test=lambda item: item % 17 == 0,
            partners=(4, 7)
        ),
        Monkey(
            items=deque([84, 98, 78, 85]),
            operation=lambda old: old * old,
            test=lambda item: item % 7 == 0,
            partners=(5, 4)
        ),
        Monkey(
            items=deque([98, 89, 78, 73, 71]),
            operation=lambda old: old + 4,
            test=lambda item: item % 2 == 0,
            partners=(3, 2)
        ),
    ]

    game = Game(monkeys)

    rounds = 20

    for _ in range(0, rounds):
        game.play_round()
    # END LOOP

    monkey_business = calculate_monkey_business(game)

    print(monkey_business)
# END MAIN
