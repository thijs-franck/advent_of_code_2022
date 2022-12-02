from os import path
from typing import Iterable, List

INPUT_PATH = path.join(path.dirname(__file__), 'data')

Round = List[str]


winning_moves = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X'
}

tied_moves = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}

shape_value = {
    'X': 1,
    'Y': 2,
    'Z': 3
}


def read_rounds(path: str) -> Iterable[Round]:
    with open(path) as file:
        for move in file:
            yield move.rstrip('\n').split(' ')
        # END LOOP
    # END WITH file
# END read_moves


def play_round(move: str, counter_move: str) -> int:
    score = shape_value[counter_move]

    if counter_move == winning_moves[move]:
        score += 6
    elif counter_move == tied_moves[move]:
        score += 3
    # END IF

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
