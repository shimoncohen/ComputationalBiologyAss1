import os
import numpy as np
from src.backend.person import Person
from utils.person import people_to_doubt_level

class BoardFileData:
    def __init__(self, cooldown, people, rumor_board) -> None:
        self.cooldown: str = cooldown
        self.people: list(str) = people
        self.rumor_board: list(str) = rumor_board

class BoardFileHandler:
    @staticmethod
    def is_data_valid(groups) -> tuple[bool, str]:
        if len(groups) < 3 or len(groups[0]) == 0 or len(groups[1]) == 0 or len(groups[2]) == 0:
            return 'File does not contain all of the needed data: cooldown, people, rumors'
        
        if not groups[0][0][0].isdigit():
            return 'The value provided for cooldown should be a positive number'

        try:
            people = np.array(groups[1])
            rumors = np.array(groups[2])
        except:
            return 'people or rumors are not a valid matrix'

        if people.shape != rumors.shape:
            return 'people and rumors should be of the same dimensions'
        
        if not np.all(np.char.isnumeric(rumors)) or not np.all(np.char.isnumeric(people)):
            return 'people and rumors should only contain numbers'
        
        flat = rumors.astype(int).flatten()
        if not (flat < 2).all():
            return 'rumor should be constructed only from 0 or 1'
        
        flat = people.astype(int).flatten()
        if not (flat < 5).all():
            return 'people should be constructed only from numbers 0 to 4'

        return ''

    @staticmethod
    def read_data(path: str) -> BoardFileData:
        with open(path) as f:
            groups = [[list(line) for line in group.split() if line] for group in f.read().split("\n\n")]
        err = BoardFileHandler.is_data_valid(groups)
        if err:
            raise Exception(f'Trying to load an invalid board file: {path}, Error: {err}')
        return BoardFileData(''.join(groups[0][0]), groups[1], groups[2])

    @staticmethod
    def load(path: str) -> tuple[np.array, np.array, bool]:
        board_data: BoardFileData = BoardFileHandler.read_data(path)
        cooldown = int(board_data.cooldown)

        people = np.array([[Person(int(doubt_level) - 1, cooldown) if int(doubt_level) > 0 else None for doubt_level in line] for line in board_data.people])
        rumor_board = np.array([[int(let) for let in line] for line in board_data.rumor_board], dtype=bool)
        return rumor_board, people
    
    @staticmethod
    def save(path: str, cooldown: int, rumor_board: np.array, people: np.array) -> None:
        people_by_doubt_level = people_to_doubt_level(people)

        list_to_str = lambda list: '\n'.join([''.join([str(int(item)) for item in row]) for row in list])
        people_string = list_to_str(people_by_doubt_level)
        rumor_board_string = list_to_str(rumor_board)

        with open(path, 'w') as f:
            f.write(f'{cooldown}{os.linesep}')
            f.writelines(people_string)
            f.write(f'{os.linesep}')
            f.writelines(rumor_board_string)
            f.write(f'{os.linesep}')
