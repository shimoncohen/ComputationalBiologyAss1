import numpy as np
from src.history.history_item import HistoryItemInterface, RumorHistoryItem
from src.history.history import History
from src.backend.game_logic import GameLogic, NeighbourCountType
from src.loader.board_file_handler import BoardFileHandler
from utils.person import count_rumors_by_people, people_to_doubt_level

class Board:
    def __init__(self, wrap_around: bool, L: int, neighbour_count_type: NeighbourCountType) -> None:
        self.L = L
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

    def initialize(self, rows: int, cols: int, p: float, doubt_probs: list[int]) -> None:
        if sum(doubt_probs) > 1:
            raise Exception('doubt probabilities should sum up to 1')
        
        self.__rumor_board = np.full((rows, cols), False)
        self.__people = np.full((rows, cols), None)
        self.__game_logic.initialize_people(self.__people, p, self.L, doubt_probs)
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
        rows, cols = self.__people.shape
        for r in range(rows):
            for c in range(cols):
                if self.__people[r, c]:
                    self.__people[r, c].update_cooldown()

    def __save_to_history(self) -> None:
        people_by_doubt_level = people_to_doubt_level(self.__people)
        people_counts = np.histogram(people_by_doubt_level, 5)[0][1:]
        rumor_counts = count_rumors_by_people(self.rumor_board, people_by_doubt_level)
        history_item = RumorHistoryItem(people_counts, rumor_counts)
        self.__history.record(history_item)
    
    def run_once(self) -> None:
        self.__update_cooldown()
        self.__rumor_board = self.__game_logic.run_once(self.__people, self.__rumor_board)
        self.__save_to_history()
        self.__generation += 1
    
    def print(self):
        print(self.__rumor_board)
    
    def get_history_csv(self):
        return self.__history.get_history_csv()
