import os
import math
import numpy as np
from src.backend.game_logic import NeighbourCountType
from src.backend.board import Board


def run(rows, cols, neighbour_count_type, wrap, s1_p, s2_p, s3_p, s4_p, p, l, iteration, run_limit=math.inf):
    file_name = fr'output\reports\wrap-{wrap}\n-{neighbour_count_type.name}\p{p}\l{l}\{s1_p}_{s2_p}_{s3_p}_{s4_p}\iteration_{iteration}.xlsx'
    if os.path.exists(file_name):
        return
    
    print(f'wrap-{wrap}\\n-{neighbour_count_type.name}\p{p}\l{l}\{s1_p}_{s2_p}_{s3_p}_{s4_p}\iteration_{iteration}')

    doubt_probs = [s1_p, s2_p, s3_p, s4_p]
    board = Board(wrap, neighbour_count_type)
    board.initialize(rows, cols, l, p, doubt_probs)

    while board.run_once() and board.total_affected < board.size and board.generation < run_limit:
        pass
    
    board.save_history(file_name)


def run_permutations(rows, cols, neighbour_count_type, wrap, run_limit=math.inf):
    S_INC = 0.2
    P_INC = 0.2
    L_LIMIT = 10

    s_ranges = np.arange(0, 1 + S_INC, S_INC)
    p_range = np.arange(P_INC, 1 + P_INC, P_INC)
    l_range = range(L_LIMIT + 1)
    i_range = range(10)
    
    for s1_p in s_ranges:
        for s2_p in s_ranges:
            for s3_p in s_ranges:
                for s4_p in s_ranges:
                    if s1_p + s2_p + s3_p + s4_p == 1:
                        for p in p_range:
                            p = round(p, 1)
                            for l in l_range:
                                for i in i_range:
                                    run(rows, cols, neighbour_count_type, wrap, s1_p, s2_p, s3_p, s4_p, p, l, i, run_limit)


def run_with_parameters(rows, cols, neighbour_count_type, wrap, s1_p, s2_p, s3_p, s4_p, p, l, run_limit=math.inf, save_history=False):
    doubt_probs = [s1_p, s2_p, s3_p, s4_p]
    board = Board(wrap, neighbour_count_type)
    board.initialize(rows, cols, l, p, doubt_probs)
    board.print()
    print()

    while board.run_once() and board.total_affected < board.size and board.generation < run_limit:
        board.print()
        print()
    
    if save_history:
        board.save_history('output/history.xlsx')


def run_from_file(path: str, neighbour_count_type: NeighbourCountType, wrap: bool, run_limit=math.inf, save_history=False):
    board = Board(wrap, neighbour_count_type)
    board.load(path)
    board.print()
    print()

    while board.run_once() and board.total_affected < board.size and board.generation < run_limit:
        board.print()
        print()
    
    if save_history:
        board.save_history('output/history.xlsx')


if __name__ == "__main__":

    BOARD_FILE_PATH = 'config/rumor_from_middle/all_s1_board.txt'
    ROWS = 100
    COLS = 100
    NEIGHBOUR_TYPE = NeighbourCountType.ALL
    WRAP = False
    GENERATION_LIMIT = 1000
    SAVE_HISTORY = False

    # Run permutations of the parameters to get all results for research
    # run_permutations(ROWS, COLS, NEIGHBOUR_TYPE, WRAP, run_limit=GENERATION_LIMIT)
    
    # Run the simulation withparameters
    run_with_parameters(ROWS, COLS, NEIGHBOUR_TYPE, WRAP, 0.25, 0.25, 0.25, 0.25, 0.6, 2, run_limit=GENERATION_LIMIT, save_history=SAVE_HISTORY)
    
    # Run the simulation with a per-defined board
    # run_from_file(BOARD_FILE_PATH, NEIGHBOUR_TYPE, WRAP, run_limit=GENERATION_LIMIT, save_history=SAVE_HISTORY)
