from src.backend.game_logic import NeighbourCountType
from src.backend.board import Board

if __name__ == "__main__":
    doubt_probs = [0.25, 0.25, 0.25, 0.25]
    board = Board(False, NeighbourCountType.ALL)
    board.initialize(5, 5, 11, 1, doubt_probs)
    # board.load('config/rumor_from_middle/all_s4_board.txt')
    board.print()
    while board.run_once():
        board.print()
        print()
