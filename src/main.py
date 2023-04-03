from backend.board import Board


if __name__ == "__main__":
    doubt_probs = [0.1, 0.1, 0.1, 0.7]
    board = Board(5, 5, 10, 1, False, doubt_probs)
    board.print()
    for _ in range(5):  
        board.run_once()
        board.print()
