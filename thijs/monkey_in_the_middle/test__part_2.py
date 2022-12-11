from collections import deque
from typing import List

from pytest import fixture

from .part_2 import Game, Monkey, calculate_monkey_business



@fixture
def monkeys() -> List[Monkey]:
    return [
        Monkey(
            items=deque([79, 98]),
            operation=lambda old: old * 19,
            test_value=23,
            partners=(2, 3)
        ),
        Monkey(
            items=deque([54, 65, 75, 74]),
            operation=lambda old: old + 6,
            test_value=19,
            partners=(2, 0)
        ),
        Monkey(
            items=deque([79, 60, 97]),
            operation=lambda old: old * old,
            test_value=13,
            partners=(1, 3)
        ),
        Monkey(
            items=deque([74]),
            operation=lambda old: old + 3,
            test_value=17,
            partners=(0, 1)
        ),
    ]
# END monkeys


def test__play_round(monkeys: List[Monkey]):

    expected_result = [
        deque([60, 71, 81, 80]),
        deque([77, 1504, 1865, 6244, 3603, 9412]),
        deque([]),
        deque([])
    ]

    game = Game(monkeys)

    game.play_round()

    items_per_monkey = [monkey.items for monkey in game.monkeys]

    assert items_per_monkey == expected_result
# END test__play_round

def test__calculate_monkey_business(monkeys: List[Monkey]):

    expected_result = 2713310158

    game = Game(monkeys)

    rounds = 10000

    for _ in range(0, rounds):
        game.play_round()
    # END LOOP

    monkey_business = calculate_monkey_business(game)

    assert monkey_business == expected_result
# END test__play_round

