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
    def is_n_on_m(arr) -> tuple[bool, str]:
        length = len(arr[0])
        return all(len(l) == length for l in arr)

    @staticmethod
    def is_data_valid(groups) -> tuple[bool, str]:
        if len(groups) < 3:
            return 'File does not contain all of the needed data: cooldown, people, rumors'

        try:
            people = np.array(groups[1])
            rumors = np.array(groups[2])
        except:
            return 'people or rumors are not a valid matrix'

        if people.shape != rumors.shape:
            return 'people and rumors should be of the same dimensions'

        return ''

    @staticmethod
    def read_data(path: str) -> BoardFileData:
        with open(path) as f:
            groups = [[list(line) for line in group.split() if line] for group in f.read().split("\n\n")]
        err = BoardFileHandler.is_data_valid(groups)
        if err:
            raise Exception(f'Trying to load an invalid board file: {path}, Error: {err}')
        return BoardFileData(groups[0][0][0], groups[1], groups[2])

    @staticmethod
    def load(path: str) -> tuple[np.array, np.array, bool]:
        board_data: BoardFileData = BoardFileHandler.read_data(path)
        cooldown = int(board_data.cooldown)

        people = np.array([[Person(int(doubt_level) - 1, cooldown) if int(doubt_level) > 0 else None for doubt_level in line] for line in board_data.people])
        rumor_board = np.array([[int(let) for let in line] for line in board_data.rumor_board], dtype=bool)
        return rumor_board, people
    
    @staticmethod
    def save(path: str, cooldown: int, rumor_board: np.array, people: np.array) -> None:
        rows, cols = people.shape
        people_by_doubt_level = [[people[r, c].doubt_level + 1 if people[r, c] else 0 for c in range(cols)] for r in range(rows)]

        list_to_str = lambda list: '\n'.join([''.join([str(int(item)) for item in row]) for row in list])
        people_string = list_to_str(people_by_doubt_level)
        rumor_board_string = list_to_str(rumor_board)

        with open(path, 'w') as f:
            f.write(f'{cooldown}{os.linesep}')
            f.writelines(people_string)
            f.write(f'{os.linesep}')
            f.writelines(rumor_board_string)
            f.write(f'{os.linesep}')
