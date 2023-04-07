import numpy as np


def people_to_doubt_level(people: np.array):
    rows, cols = people.shape
    return np.array([[people[r, c].doubt_level + 1 if people[r, c] else 0 for c in range(cols)] for r in range(rows)])