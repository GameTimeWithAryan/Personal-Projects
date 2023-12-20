from ttt_engine import Board
from ttt_engine.board import evaluate_position
import cProfile
import pstats
from random import randint

if __name__ == '__main__':

    with cProfile.Profile() as pr:
        board = Board(4)
        for i in range(6):
            # COMPLETE ME
            board.play_move(randint())
        board.grid.print_grid()
        evaluate_position(board)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
