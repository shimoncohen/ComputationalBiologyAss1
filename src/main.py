from backend.board import Board
from loader.board_loader import BoardLoader

if __name__ == "__main__":
    doubt_probs = [0.1, 0.1, 0.1, 0.7]
    board = Board(False, 10)
    board.initialize(5, 5, 1, doubt_probs)
    # board.load('src/config/board.txt')
    board.print()
    for _ in range(5):  
        board.run_once()
        board.print()
