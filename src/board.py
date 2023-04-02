import random
import numpy as np
from game_logic import GameLogic

class Board:
    def __init__(self, rows: int, cols: int, L: int, p: float, wrap_around: bool, doubt_probs: list[int]) -> None:
        self.L = L
        self.p = p
        self.game_logic = GameLogic(wrap_around)
        self.generation = 0
        
        self.rumor_board = np.full((rows, cols), False)
        self.people = np.full((rows, cols), None)
        self.game_logic.initialize_people(self.people, self.p, self.L, doubt_probs)

        # Initialize one random person to spread rumor
        row, col = random.randrange(rows), random.randrange(cols)
        self.rumor_board[row, col] = True

    def get_rumors(self) -> np.array:
        return self.rumor_board

    def get_people(self) -> np.array:
        return self.people
    
    def update_cooldown(self):
        for p in self.people:
            p.update_cooldown()
    
    def run_once(self) -> None:
        self.update_cooldown()
        self.rumor_board = self.game_logic.run_once(self.people, self.rumor_board)
        self.generation += 1
    
    def print(self):
        print(self.rumor_board)
