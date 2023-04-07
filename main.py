from backend.game_logic import NeighbourCountType
from src.backend.board import Board

if __name__ == "__main__":
    doubt_probs = [0.1, 0.1, 0.1, 0.7]
    board = Board(False, 10, NeighbourCountType.ALL)
    # board.initialize(5, 5, 1, doubt_probs)
    board.load('src/config/rumor_from_middle/all_s4_board.txt')
    board.print()
    for _ in range(5):  
        board.run_once()
        board.print()
