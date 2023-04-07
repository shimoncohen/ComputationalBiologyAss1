import random
import numpy as np
from src.backend.dimensions import clip, wrap
from src.backend.person import DoubtLevel, Person

class GameLogic:
    def __init__(self, wrap_around: bool) -> None:
        self.__wrap_around: bool = wrap_around
        self.__idx_func: callable = wrap if self.__wrap_around else clip
    
    def initialize_people(self, people: np.array, p: int, L:int, doubt_probs: list[int]):
        rows, cols = people.shape
        for r in range(rows):
            for c in range(cols):
                prob = random.uniform(0, 1)
                if prob <= p:
                    doubt_level = self._generate_doubt_level(doubt_probs)
                    people[r, c] = Person(doubt_level, L)
    
    def _generate_doubt_level(self, doubt_probs: list[int]) -> DoubtLevel:
        # prob = random.uniform(0, 1)
        # prob_thresholds = [sum(doubt_probs[:i + 1]) for i in range(len(doubt_probs))]
        # doubt_level = next(x for x, p in enumerate(prob_thresholds) if p > prob)
        doubt_level = random.choices([d.value for d in DoubtLevel], weights=doubt_probs)[0]
        return DoubtLevel(doubt_level)

    def run_once(self, people: np.array, rumors: np.array) -> np.array:
        rumor_board = np.full(rumors.shape, False)
        rows, cols = rumors.shape

        for p in people[np.where(rumors)]:
            p.activate_cooldown()

        for r in range(rows):
            for c in range(cols):
                count = self._count_rumors(rumors, r, c)
                if people[r, c] is not None:
                    rumor_board[r, c] = people[r, c].should_pass_rumor(count)
        
        return rumor_board

    def _count_rumors(self, rumors: np.array, row: int, col: int):
        rows, cols = rumors.shape
        idxs = self._generate_neighbour_idxs(row, col)
        idxs = self.__idx_func(idxs, rows, cols)
        values = np.array([rumors[row, col] for row, col in idxs])
        return values.sum()
    
    def _generate_neighbour_idxs(self, row, col):
        return [
            [r, c]
            for r in range(row - 1, row + 2)
            for c in range(col - 1, col + 2)
            if r != row or c != col
        ]
