import math
import numpy as np
from src.backend.person import DoubtLevel
from src.history.history_item import RumorHistoryItem
from src.history.history import History
from src.backend.game_logic import GameLogic, NeighbourCountType
from src.loader.board_file_handler import BoardFileHandler
from utils.person import count_rumors_by_people, people_to_doubt_level
from typing import List

class Board:
    """
    Holds the simulation layout.
    """
    def __init__(self, wrap_around: bool, neighbour_count_type: NeighbourCountType) -> None:
        self.__game_logic = GameLogic(wrap_around, neighbour_count_type)
        self.__history: History[RumorHistoryItem] = History[RumorHistoryItem]()

        self.__generation = 0
        self.__rumor_board = None
        self.__people = None
    
    @property
    def generation(self):
        return self.__generation
    
    @property
    def rumor_board(self):
        return self.__rumor_board
    
    @property
    def people(self):
        return self.__people
    
    @property
    def total_affected(self):
        return self.__game_logic.get_total_affected(self.people)

    @property
    def shape(self):
        return self.__rumor_board.shape
    
    @property
    def size(self):
        return self.__rumor_board.size

    def initialize(self, rows: int, cols: int, L: int, p: float, doubt_probs: List[int]) -> None:
        """
        Initialize the board with given parameters.

        Args:
            rows (int): num of rows in the board
            cols (int): num of columns in the board
            L (int): number of generations a person should not pass a rumor after receiving one
            p (float): wanted pupulation density
            doubt_probs (List[int]): propabilities for each doubt level

        Raises:
            Exception: raised if doubt probabilities do not sum up to 1
            Exception: raised if p > 1 or p < 0
        """
        if math.ceil(sum(doubt_probs)) > 1:
            raise Exception('doubt probabilities should sum up to 1')
        if p > 1 or p < 0:
            raise Exception('population density cannot be greater than 1')
        
        self.__rumor_board = np.full((rows, cols), False)
        self.__people = np.full((rows, cols), None)
        self.__game_logic.initialize_people(self.__people, p, L, doubt_probs)
        self.__initialize_random_rumor()
        self.__save_to_history()
    
    def __initialize_random_rumor(self) -> None:
        idxs = np.argwhere(self.people)
        i = np.random.randint(idxs.shape[0])
        row, col = idxs[i]
        self.__rumor_board[row, col] = True
    
    def load(self, path: str) -> None:
        self.__rumor_board, self.__people = BoardFileHandler.load(path)
        self.__save_to_history()
    
    def save(self, path: str) -> None:
        BoardFileHandler.save(path, self.L, self.__rumor_board, self.__people)
    
    def __update_cooldown(self):
        """
        Update the cooldown of all the people in the board.
        """
        rows, cols = self.__people.shape
        for r in range(rows):
            for c in range(cols):
                if self.__people[r, c]:
                    self.__people[r, c].update_cooldown()

    def __save_to_history(self) -> None:
        people_by_doubt_level = people_to_doubt_level(self.__people)
        # Number of bins should include the bin edges and start from 1 (first doubt level)
        num_bins = range(1, len(DoubtLevel) + 2)
        people_counts = np.histogram(people_by_doubt_level, num_bins)[0]
        rumor_counts = count_rumors_by_people(self.rumor_board, people_by_doubt_level)
        history_item = RumorHistoryItem(people_counts, rumor_counts, self.total_affected)
        self.__history.record(history_item)
    
    def run_once(self) -> bool:
        """
        Run one round of the simulation.

        Returns:
            bool: can the simulation continue
        """
        self.__update_cooldown()
        next = self.__game_logic.run_once(self.__people, self.__rumor_board)
        if (next == self.__rumor_board).all():
            return False
        self.__rumor_board = next
        self.__save_to_history()
        self.__generation += 1
        return True
    
    def print(self):
        rows, cols = self.__rumor_board.shape
        [print(['x' if self.rumor_board[r, c] else '-' for c in range(cols)]) for r in range(rows)]
    
    def get_history_csv(self) -> List[str]:
        """
        Get the board history as CSV format.

        Returns:
            List[str]: history as CSV lines
        """
        return self.__history.get_history_csv()
    
    def save_history(self, path: str) -> None:
        """
        Save board history to file.

        Args:
            path (str): path to save the file to
        """
        self.__history.save(path)
