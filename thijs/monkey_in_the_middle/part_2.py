from collections import deque
from dataclasses import dataclass, field
from math import prod
from typing import Callable, Deque, Iterable, List, Tuple

WorryLevel = int
Operation = Callable[[WorryLevel], WorryLevel]
Test = Callable[[WorryLevel], bool]
Partners = Tuple[int, int]
Throw = Tuple[int, WorryLevel]


@dataclass
class Monkey:
    operation: Operation
    test_value: int
    partners: Partners

    inspections = 0
    items: Deque[WorryLevel] = field(default_factory=deque)

    def inspect(self, item: WorryLevel) -> WorryLevel:
        self.inspections += 1
        return self.operation(item)
    # END inspect

    def test(self, item: WorryLevel) -> bool:
        return item % self.test_value == 0
    # END test

    def take_turn(self) -> Iterable[Throw]:
        while len(self.items) > 0:
            item = self.items.popleft()

            worry_level = self.inspect(item)
            passes_test = self.test(worry_level)
            partner = self.partners[0] if passes_test else self.partners[1]

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

    _divisor: int = field(init=False)

    def __post_init__(self):
        self._divisor = prod(monkey.test_value for monkey in self.monkeys)
    # END __post_init__

    def play_round(self):
        self.round += 1
        for monkey in self.monkeys:
            self.turn += 1
            for partner, item in monkey.take_turn():
                self.monkeys[partner].catch_item(item % self._divisor)
            # END LOOP
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
            test_value=11,
            partners=(6, 5)
        ),
        Monkey(
            items=deque([57, 88, 80]),
            operation=lambda old: old + 5,
            test_value=19,
            partners=(6, 0)
        ),
        Monkey(
            items=deque([61, 81, 84, 69, 77, 88]),
            operation=lambda old: old * 19,
            test_value=5,
            partners=(3, 1)
        ),
        Monkey(
            items=deque([78, 89, 71, 60, 81, 84, 87, 75]),
            operation=lambda old: old + 7,
            test_value=3,
            partners=(1, 0)
        ),
        Monkey(
            items=deque([60, 76, 90, 63, 86, 87, 89]),
            operation=lambda old: old + 2,
            test_value=13,

            partners=(2, 7)
        ),
        Monkey(
            items=deque([88]),
            operation=lambda old: old + 1,
            test_value=17,
            partners=(4, 7)
        ),
        Monkey(
            items=deque([84, 98, 78, 85]),
            operation=lambda old: old * old,
            test_value=7,
            partners=(5, 4)
        ),
        Monkey(
            items=deque([98, 89, 78, 73, 71]),
            operation=lambda old: old + 4,
            test_value=2,
            partners=(3, 2)
        ),
    ]

    game = Game(monkeys)

    rounds = 10000

    for _ in range(0, rounds):
        game.play_round()
    # END LOOP

    monkey_business = calculate_monkey_business(game)

    print(monkey_business)
# END MAIN
