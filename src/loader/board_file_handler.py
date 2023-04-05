import os
import re
import numpy as np
from src.backend.person import Person

class BoardFileData:
    def __init__(self, cooldown, people, rumor_board) -> None:
        self.cooldown: str = cooldown
        self.people: list(str) = people
        self.rumor_board: list(str) = rumor_board

class BoardFileHandler:
    @staticmethod
    def read_data(path: str) -> BoardFileData:
        with open(path) as f:
            groups = [[line for line in group.split() if line] for group in f.read().split("\n\n")]
        return BoardFileData(groups[0][0], groups[1], groups[2])

    @staticmethod
    def load(path: str) -> tuple[np.array, np.array, bool]:
        board_data: BoardFileData = BoardFileHandler.read_data(path)
        cooldown = int(board_data.cooldown)

        people = np.array([[Person(int(doubt_level) - 1, cooldown) for doubt_level in line] for line in board_data.people])
        rumor_board = np.array([[int(let) for let in list(line)] for line in board_data.rumor_board], dtype=bool)
        return rumor_board, people
    
    @staticmethod
    def save(path: str, cooldown: int, rumor_board: np.array, people: np.array) -> None:
        rows, cols = people.shape
        people_by_doubt_level = [[people[r, c].doubt_level + 1 for c in range(cols)] for r in range(rows)]

        list_to_str = lambda list: '\n'.join([''.join([str(int(item)) for item in row]) for row in list])
        people_string = list_to_str(people_by_doubt_level)
        rumor_board_string = list_to_str(rumor_board)

        with open(path, 'w') as f:
            f.write(f'{cooldown}{os.linesep}')
            f.writelines(people_string)
            f.write(f'{os.linesep}')
            f.writelines(rumor_board_string)
            f.write(f'{os.linesep}')
