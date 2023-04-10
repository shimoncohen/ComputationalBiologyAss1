import pytest
import numpy as np
from typing import Tuple
from src.backend.game_logic import NeighbourCountType
from src.backend.board import Board


@pytest.fixture()
def initialize_board(wrap_around, L, rows, cols, doubt_probs):
    board = Board(wrap_around, NeighbourCountType.ALL)
    board.initialize(rows, cols, L, 1, doubt_probs)
    return board

@pytest.fixture()
def load_board(fs_no_root, wrap_around, path, L, people, rumors) -> Tuple[Board, str]:
    fs_no_root.create_file(path, contents=f"""{L}\n\n{people}\n\n{rumors}\n\n""")
    board = Board(wrap_around, NeighbourCountType.ALL)
    try:
        board.load(path)
    except Exception as e:
        return None, e
    return board, ''


class Helpers:
    @staticmethod
    def get_cooldown_arr(board: Board):
        rows, cols = board.people.shape
        return np.array([board.people[r, c].cooldown for r in range(rows) for c in range(cols)])


class TestBoard():
    @pytest.mark.parametrize(
        "wrap_around, L, rows, cols, doubt_probs",
        [
            pytest.param(True, 5, 10, 10, [0.25, 0.25, 0.25, 0.25]),
        ]
    )
    def test_board_initializes_correctly(self, initialize_board, L):
        board = initialize_board
        rows, cols = board.people.shape

        # Make sure all people are defined
        assert all([[board.people[r, c] is not None for c in range(cols)] for r in range(rows)])

        # Make sure all people have the correct cooldown value
        assert all([[board.people[r, c].cooldown == L for c in range(cols)] for r in range(rows)])

        # Make sure only one person is about to pass the rumor
        count = board.rumor_board.sum()
        assert count == 1
    
    @pytest.mark.parametrize(
        "wrap_around, path, L, people, rumors",
        [
            pytest.param(
                True,
                '/path/to/text.txt',
                '10',
                '4',
                '1'
            ),
        ]
    )
    def test_board_loads_correctly(self, load_board, L):
        board, _ = load_board
        rows, cols = board.people.shape

        # Make sure all people are defined
        assert all([[board.people[r, c] is not None for c in range(cols)] for r in range(rows)])

        # Make sure all people have the correct cooldown value
        assert all([[board.people[r, c].cooldown == L for c in range(cols)] for r in range(rows)])

        # Make sure only one person is about to pass the rumor
        count = board.rumor_board.sum()
        assert count == 1
    
    @pytest.mark.parametrize(
        "wrap_around, path, L, people, rumors, error",
        [
            pytest.param(
                True,
                '/path/to/text.txt', '',
                '',
                '',
                'Trying to load an invalid board file: /path/to/text.txt, Error: File does not contain all of the needed data: cooldown, people, rumors'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '10',
                '',
                '',
                'Trying to load an invalid board file: /path/to/text.txt, Error: File does not contain all of the needed data: cooldown, people, rumors'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '',
                '4',
                '1',
                'Trying to load an invalid board file: /path/to/text.txt, Error: File does not contain all of the needed data: cooldown, people, rumors'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', 'c',
                '',
                '',
                'Trying to load an invalid board file: /path/to/text.txt, Error: File does not contain all of the needed data: cooldown, people, rumors'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', 'c',
                '4',
                '1',
                'Trying to load an invalid board file: /path/to/text.txt, Error: The value provided for cooldown should be a positive number'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '-1',
                '4',
                '1',
                'Trying to load an invalid board file: /path/to/text.txt, Error: The value provided for cooldown should be a positive number'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                4
                404
                """,
                '1',
                'Trying to load an invalid board file: /path/to/text.txt, Error: people or rumors are not a valid matrix'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                404
                404
                """,
                """
                001
                10
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: people or rumors are not a valid matrix'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                4044
                4044
                """,
                """
                001
                101
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: people and rumors should be of the same dimensions'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                40s4
                4044
                """,
                """
                0011
                1011
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: people and rumors should only contain numbers'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                4044
                4044
                """,
                """
                0011
                1c11
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: people and rumors should only contain numbers'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                4045
                6044
                """,
                """
                0011
                1011
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: people should be constructed only from numbers 0 to 4'
            ),
            pytest.param(
                True,
                '/path/to/text.txt', '5',
                """
                4044
                4044
                """,
                """
                0021
                4011
                """,
                'Trying to load an invalid board file: /path/to/text.txt, Error: rumor should be constructed only from 0 or 1'
            ),
        ]
    )
    def test_board_load_raises(self, load_board, error):
        _, e = load_board
        print(e)
        assert str(e) == error
    
    @pytest.mark.parametrize(
        "wrap_around, L, rows, cols, doubt_probs",
        [
            pytest.param(True, 5, 10, 10, [0.25, 0.25, 0.25, 0.25]),
            pytest.param(False, 2, 4, 7, [0.25, 0.25, 0.25, 0.25])
        ]
    )
    def test_update_cooldown(self, initialize_board):
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
