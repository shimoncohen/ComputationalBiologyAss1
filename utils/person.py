import numpy as np


def people_to_doubt_level(people: np.array) -> np.array:
    rows, cols = people.shape
    return np.array([[people[r, c].doubt_level + 1 if people[r, c] else 0 for c in range(cols)] for r in range(rows)])

def people_to_doubt_level_csv(people: np.array) -> np.array:
    rows, cols = people.shape
    return '\n'.join([','.join([people[r, c].doubt_level.name if people[r, c] else '0' for c in range(cols)]) for r in range(rows)])

def count_rumors_by_people(rumor_board: np.array, people_by_doubt_level: np.array) -> list:
    rows, cols = rumor_board.shape
    rumors = [0, 0, 0, 0]
    for r in range(rows):
        for c in range(cols):
            doubt_level = people_by_doubt_level[r, c]
            if people_by_doubt_level[r, c] != 0 and rumor_board[r, c]:
                rumors[doubt_level - 1] += 1
    return rumors
