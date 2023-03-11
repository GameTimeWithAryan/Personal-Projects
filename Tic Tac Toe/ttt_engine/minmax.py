from math import inf
from typing import TypeAlias

from .grid import Coordinate

Board: TypeAlias = 'Board'


def minmax(minmax_board: Board, maximizing: bool = True, evaluating: bool = False):
    """ Minmax AI for Tic Tac Toe

    It uses the MinMax Algorithm to either get the best move
    or the current evaluation of the position with best play by both sides

    Parameters
    ----------
        minmax_board : Board
            A copy of the original board
        maximizing : bool
            Maximizing or the Minimizing player in minmax algorithm
        evaluating : bool
            When evaluating is True, returns the evaluation of the position
            When evaluating is False, returns the best move on the board """

    min_eval = inf
    max_eval = -inf
    best_move: Coordinate | None = None

    # BASE CASES
    if minmax_board.state.check_win(minmax_board.get_other_player()):
        if evaluating:
            # If current player is the maximizing player then it means the other player played the winning move
            # Hence it returns -1 as eval, and vice versa
            return -1 if maximizing else 1
        else:
            return None

    if minmax_board.state.check_draw():
        return 0 if evaluating else None

    # MINMAX ALGORITHM
    for move in minmax_board.grid.get_legal_moves():
        evaluation = evaluate(minmax_board, move, not maximizing)
        if maximizing:
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            # If the best move is found for maximizing player then return
            # No need to check for other moves as any other move cannot be better than eval of +1
            if max_eval == 1:
                return max_eval if evaluating else best_move

        elif not maximizing:
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            if min_eval == -1:
                return min_eval if evaluating else best_move

    if evaluating:
        return max_eval if maximizing else min_eval
    return best_move


def evaluate(board: Board, move: Coordinate, maximizing: bool):
    """Evaluates the move and returns the evaluation
    Parameters
    ----------
        board : Board
            board object to make a move on, must be a copy to prevent changing data of the actual board
        move : Coordinate
            coordinates (row, column) of the move to evaluate
        maximizing : bool
            boolean to tell to evaluate from the maximizing size or the minimizing side"""

    board.play_move(move[0], move[1])
    evaluation = minmax(board, maximizing, evaluating=True)
    board.play_move(move[0], move[1], unplay=True)
    return evaluation
