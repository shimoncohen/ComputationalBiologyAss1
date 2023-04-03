import random
import numpy as np
from backend.game_logic import GameLogic
from loader.board_loader import BoardLoader

class Board:
    def __init__(self, wrap_around: bool, L: int) -> None:
        self.L = L
        self.game_logic = GameLogic(wrap_around)
        self.generation = 0

        self.rumor_board = None
        self.people = None

    def initialize(self, rows: int, cols: int, p: float, doubt_probs: list[int]) -> None:
        self.rumor_board = np.full((rows, cols), False)
        self.people = np.full((rows, cols), None)
        self.game_logic.initialize_people(self.people, p, self.L, doubt_probs)
        self._initialize_random_rumor(rows, cols)
    
    def _initialize_random_rumor(self, rows, cols) -> None:
        # Initialize one random person to spread rumor
        row, col = random.randrange(rows), random.randrange(cols)
        self.rumor_board[row, col] = True
    
    def load(self, path: str) -> None:
        self.rumor_board, self.people = BoardLoader.Load(path)

    def get_rumors(self) -> np.array:
        return self.rumor_board

    def get_people(self) -> np.array:
        return self.people
    
    def update_cooldown(self):
        rows, cols = self.people.shape
        for r in range(rows):
            for c in range(cols):
                self.people[r, c].update_cooldown()
    
    def run_once(self) -> None:
        self.update_cooldown()
        self.rumor_board = self.game_logic.run_once(self.people, self.rumor_board)
        self.generation += 1
    
    def print(self):
        print(self.rumor_board)
        # rows, cols = self.people.shape
        # for r in range(rows):
        #     for c in range(cols):
        #         if self.people[r, c] is not None:
        #             print(self.people[r, c].doubt_level, end=' ')
        #         else:
        #             print(None, end=' ')
        #     print()
