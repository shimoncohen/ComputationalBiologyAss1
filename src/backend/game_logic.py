import random
import numpy as np
from typing import Callable
from enum import IntEnum
from src.backend.dimensions import clip, wrap
from src.backend.person import DoubtLevel, Person

class NeighbourCountType(IntEnum):
    ALL = 0
    CROSS = 1
    DIAGONAL = 2

    def get_strategy(neighbour_count_type: int) -> Callable[[int, int, int, int], bool]:
        match neighbour_count_type:
            case 1:
                return lambda row, col, r, c: r != row and c != col
            case 2:
                return lambda row, col, r, c: r == row or c == col
            case _:
                return lambda row, col, r, c: r != row or c != col

class GameLogic:
    def __init__(self, wrap_around: bool, neighbour_count_type: NeighbourCountType) -> None:
        self.__wrap_around: bool = wrap_around
        self.__idx_fix_func: callable = wrap if self.__wrap_around else clip
        self.__neighbour_count_strategy: Callable[[int, int, int, int], bool] = NeighbourCountType.get_strategy(neighbour_count_type)
    
    def initialize_people(self, people: np.array, p: int, L:int, doubt_probs: list[int]):
        rows, cols = people.shape
        for r in range(rows):
            for c in range(cols):
                prob = random.uniform(0, 1)
                if prob <= p:
                    doubt_level = self._generate_doubt_level(doubt_probs)
                    people[r, c] = Person(doubt_level, L)
    
    def _generate_doubt_level(self, doubt_probs: list[int]) -> DoubtLevel:
        doubt_level = random.choices([d.value for d in DoubtLevel], weights=doubt_probs)[0]
        return DoubtLevel(doubt_level)

    def run_once(self, people: np.array, rumors: np.array) -> np.array:
        rumor_board = np.full(rumors.shape, False)
        rows, cols = rumors.shape

        for p in people[np.where(rumors)]:
            p.activate_cooldown()

        for r in range(rows):
            for c in range(cols):
                count = self.__count_rumors(rumors, r, c)
                if people[r, c] is not None:
                    rumor_board[r, c] = people[r, c].should_pass_rumor(count)
        
        return rumor_board

    def __count_rumors(self, rumors: np.array, row: int, col: int):
        rows, cols = rumors.shape
        idxs = self.__generate_neighbour_idxs(row, col, 2)
        idxs = self.__idx_fix_func(idxs, rows, cols)
        values = np.array([rumors[row, col] for row, col in idxs])
        return values.sum()
    
    def __generate_neighbour_idxs(self, row: int, col: int, neighbour_count_type: NeighbourCountType):
        return [
            [r, c]
            for r in range(row - 1, row + 2)
            for c in range(col - 1, col + 2)
            if self.__neighbour_count_strategy(row, col, r, c)
        ]
