"""
Main Module for using the tic tac toe engine
Contains Board class to control the board and play the game

Usage
-----
Defining a board:
`game_board = Board()`

Board setup for custom use:
`custom_board = Board()
custom_board.grid.grid = [[custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL]]
custom_board.fix_attributes()`

Here custom_board.EMPTY_CELL can be swapped for any mark from the custom_board.players list
Then fix_attributes method is run to select which player's turn it is and update Grid.has_moved attribute
"""

import copy
from math import inf
from colorama import Fore

from .grid import Grid, Coordinate
from .state_checker import StateChecker


class Board:
    """Board class for managing the game

    Contains methods for playing a complete tic tac toe game whilst automatically managing
    player turns and having extra data like `has_moved attribute` of grid class if required

    Attributes
    ----------
        player_index : int
            Current player index, keeps track of whose turn to move is it
        players : list[str]
            A list of marks which will be used to play the game
            When a move is played, the board will be updated using these marks
        grid : Grid
            Instance of Grid class for managing the grid
        state : StateChecker
            Instance of StateChecker to check wins or draws and update win_data accordingly
    """

    def __init__(self, size: int = 3):
        self.player_index: int = 0
        self.players: list[str] = ["X", "O"]

        self.grid: Grid = Grid(size)
        self.state: StateChecker = StateChecker(self.grid)

    def reset(self):
        self.__init__(self.grid.size)

    def play_move(self, row: int, column: int, unplay: bool = False):
        """Plays a move on the grid and updates current player

        Parameters
        ----------
            row : int
                Row number on which to play the move
            column : int
                Column number on which to play the move
            unplay : bool
                If True, play_move marks an Empty cell on the given coordinate i.e. unplays the move
                If False, marks the player whose turn it was on the given coordinate"""

        mark = self.get_current_player()
        if unplay:
            mark = self.grid.EMPTY_CELL

        self.grid.update_cell(row, column, mark)
        self.grid.update_has_moved()
        self.switch_player()

    def get_current_player(self) -> str:
        """Get the mark of current player"""
        return self.players[self.player_index]

    def get_other_player(self) -> str:
        """Get the mark of the player other than the current player"""
        return self.players[self.get_other_player_index()]

    def get_other_player_index(self) -> int:
        return int(not self.player_index)

    def switch_player(self):
        """Change current player index to the other player"""
        self.player_index = self.get_other_player_index()

    def fix_attributes(self):
        """Manually fix/assign attributes of the class by checking the board state
            Must be run when working with custom setup"""

        self.grid.update_has_moved()

        if len(self.grid.get_legal_moves()) % 2 == 1:
            self.player_index = 0
        else:
            self.player_index = 1

    def ai_play(self):
        """Use the minmax AI function to get the best move and play it"""
        # Creating a copy of board to avoid the updating the win_data while trying to find best moves
        # as minmax board requires to play many moves and check for win which would update win data of board
        minmax_board = copy.deepcopy(self)
        move = minmax(minmax_board, maximizing=True, evaluating=False)  # Get best move
        if type(move) == tuple:
            self.play_move(move[0], move[1])


##################### AI ###########################

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

    if minmax_board.state.check_win(minmax_board.get_other_player()):
        # If current player is the maximizing player then it means the other player played the winning move
        # Hence it returns -1 as eval, and vice versa
        return -1 if maximizing else 1
    if minmax_board.state.check_draw():
        return 0

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
    evaluation = minmax(board, maximizing=maximizing, evaluating=True)
    board.play_move(move[0], move[1], unplay=True)
    return evaluation


################## CUSTOM SETUP #########################
def evaluate_position(board: Board):
    """Evaluates each legal move and prints it with the grid telling eval of each move

    Parameters
    ----------
    board : Board
        board to evaluate"""

    str_evaluations: list[str] = []
    legal_moves = board.grid.get_legal_moves()

    if board.player_index == 0:
        eval_color_coding = {"0": Fore.BLUE, "1": Fore.GREEN, "-1": Fore.RED}
    else:
        eval_color_coding = {"0": Fore.BLUE, "1": Fore.RED, "-1": Fore.GREEN}

    for move in legal_moves:
        str_evaluation = str(evaluate(board, move, bool(board.player_index)))
        str_evaluation = eval_color_coding[str_evaluation] + str_evaluation + Fore.RESET
        str_evaluations.append(str_evaluation)

    eval_grid = copy.deepcopy(board.grid)
    for index, (row, column) in enumerate(legal_moves):
        eval_grid.update_cell(row, column, str_evaluations[index])

    # PRINTING
    eval_grid.print_grid()
    print(f"Player Turn: {board.get_current_player()}\n")
    print(" 0 - Draw")
    print(f" 1 - {board.players[0]} Wins")
    print(f"-1 - {board.players[1]} Wins")
