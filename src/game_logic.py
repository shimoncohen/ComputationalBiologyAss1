import numpy as np
from dimensions import clip, remove_exeeding

class GameLogic:
    def __init__(self, wrap_around: bool) -> None:
        self.wrap_around: bool = wrap_around
        self.mode: str = 'wrap' if wrap_around else 'clip'
        self.idx_func: function = clip if self.wrap_around else remove_exeeding

    def run_once(people: np.array, rumors: np.array) -> np.array:
        pass

    def _count_rumors(self, rumors: np.array, row: int, col: int):
        rows, cols = rumors.shape
        idxs = self._generate_neighbour_idxs(row, col)
        idxs = self.idx_func(idxs, rows, cols)
        values = np.array([rumors[row, col] for row, col in idxs])
        return values.sum()
    
    def _generate_neighbour_idxs(self, row, col):
        return [
            [r, c]
            for r in range(row - 1, row + 2)
            for c in range(col - 1, col + 2)
            if r != row or c != col
        ]
    

a = np.array([[True, False, False], 
              [True, False, True], 
              [False, False, False]])
print(GameLogic._count_rumors(GameLogic(True), a, 0, 0))