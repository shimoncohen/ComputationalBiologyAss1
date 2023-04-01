import numpy as np
from game_logic import GameLogic

class Board:
    def __init__(self, row: int, col: int, L: int, p: float, wrap_around: bool) -> None:
        self.L = L
        self.p = p
        self.game_logic = GameLogic(wrap_around)
        
        self.rumor_board = np.full((row, col), False)
        self.people = np.full((row, col), None)