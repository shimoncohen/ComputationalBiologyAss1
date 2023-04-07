import random
import numpy as np
from src.backend.game_logic import GameLogic
from src.loader.board_file_handler import BoardFileHandler

class Board:
    def __init__(self, wrap_around: bool, L: int) -> None:
        self.L = L
        self.__game_logic = GameLogic(wrap_around)
        self.generation = 0

        self.__rumor_board = None
        self.__people = None
    
    @property
    def rumor_board(self):
        return self.__rumor_board
    
    @property
    def people(self):
        return self.__people

    def initialize(self, rows: int, cols: int, p: float, doubt_probs: list[int]) -> None:
        self.__rumor_board = np.full((rows, cols), False)
        self.__people = np.full((rows, cols), None)
        self.__game_logic.initialize_people(self.__people, p, self.L, doubt_probs)
        self.__initialize_random_rumor(rows, cols)
    
    def __initialize_random_rumor(self, rows, cols) -> None:
        # Initialize one random person to spread rumor
        # row, col = random.randrange(rows), random.randrange(cols)
        idxs = np.argwhere(self.people)
        i = np.random.randint(idxs.shape[0])
        row, col = idxs[i]
        self.__rumor_board[row, col] = True
    
    def load(self, path: str) -> None:
        self.__rumor_board, self.__people = BoardFileHandler.load(path)
    
    def save(self, path: str) -> None:
        BoardFileHandler.save(path, self.L, self.__rumor_board, self.__people)
    
    def __update_cooldown(self):
        rows, cols = self.__people.shape
        for r in range(rows):
            for c in range(cols):
                if self.__people[r, c]:
                    self.__people[r, c].update_cooldown()
    
    def run_once(self) -> None:
        self.__update_cooldown()
        self.__rumor_board = self.__game_logic.run_once(self.__people, self.__rumor_board)
        self.generation += 1
    
    def print(self):
        print(self.__rumor_board)
