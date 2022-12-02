from os import path
from typing import Callable, Dict, Iterable, List

INPUT_PATH = path.join(path.dirname(__file__), 'data')


Round = List[str]
Strategy = Callable[[str], int]


shape_value = {
    'A': 1,
    'B': 2,
    'C': 3
}

winning_moves = {
    'A': 'B',
    'B': 'C',
    'C': 'A'
}

losing_moves = {
    'A': 'C',
    'B': 'A',
    'C': 'B'
}

strategies: Dict[str, Strategy] = {
    'X': lambda move: shape_value[losing_moves[move]],
    'Y': lambda move: 3 + shape_value[move],
    'Z': lambda move: 6 + shape_value[winning_moves[move]]
}


def read_rounds(path: str) -> Iterable[Round]:
    with open(path) as file:
        for move in file:
            yield move.rstrip('\n').split(' ')
        # END LOOP
    # END WITH file
# END read_moves


def play_round(move: str, strategy_name: str) -> int:
    strategy = strategies[strategy_name]
    score = strategy(move)
    return score
# END play_round


def calculate_total_score(rounds: Iterable[Round]):
    return sum(play_round(*round) for round in rounds)
# END calculate_total score


if __name__ == '__main__':
    rounds = read_rounds(INPUT_PATH)
    total_score = calculate_total_score(rounds)

    print(total_score)
# END MAIN
