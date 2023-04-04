import numpy as np
from backend.person import Person

class BoardLoader:
    @staticmethod
    def Load(path: str) -> tuple[np.array, np.array, bool]:
        with open(path) as f:
            row, col = f.readline().split()
            cooldown = int(f.readline())
            people = np.array([[Person(int(doubt_level) - 1, cooldown) for doubt_level in line.strip()] for line in f.readlines()])

        rows, cols = people.shape
        rumor_board = np.full((rows, cols), False)
        rumor_board[int(row), int(col)] = True

        return rumor_board, people
