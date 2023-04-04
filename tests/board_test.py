import pytest
import numpy as np
from src.backend.board import Board

@pytest.fixture()
def initialize_board(wrap_around, L, rows, cols, doubt_probs):
    board = Board(wrap_around, L)
    board.initialize(rows, cols, 1, doubt_probs)
    return board

class Helpers:
    @staticmethod
    def get_cooldown_arr(board: Board):
        rows, cols = board.people.shape
        return np.array([board.people[r, c].cooldown for r in range(rows) for c in range(cols)])

class TestBoard:
    @pytest.mark.parametrize(
        "wrap_around, L, rows, cols, doubt_probs",
        [
            pytest.param(True, 5, 10, 10, [0.25, 0.25, 0.25, 0.25]),
        ]
    )
    def test_board_initializes_correctly(self, initialize_board, L):
        board = initialize_board

        # Make sure all people are defined
        assert all([p is not None for p in board.people])

        # Make sure only one person is about to pass the rumor
        count = board.rumor_board.sum()
        assert count == 1

        assert board.L == L
    
    @pytest.mark.parametrize(
        "wrap_around, L, rows, cols, doubt_probs",
        [
            pytest.param(True, 5, 10, 10, [0.25, 0.25, 0.25, 0.25]),
            pytest.param(False, 2, 4, 7, [0.25, 0.25, 0.25, 0.25])
        ]
    )
    def test_update_cooldown(self, initialize_board, L):
        board: Board = initialize_board
        
        # Run a few generations
        for _ in range(10):
            board.run_once()
        cooldowns = Helpers.get_cooldown_arr(board)
        board.run_once()
        updated_cooldowns = Helpers.get_cooldown_arr(board)

        # Get all people that had cooldown in the last generation
        idxs = np.argwhere(cooldowns != 0)
        # Check that cooldown was updated correctly
        assert all([ max(c - 1, 0) == u_c for c, u_c in zip(cooldowns[idxs], updated_cooldowns[idxs])])
