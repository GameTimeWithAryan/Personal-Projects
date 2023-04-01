"""
ttt_engine.board
~~~~~~~~~~~~~~~~

Main Module for using the tic tac toe engine
Contains Board class to control the board and play the game

Usage
-----
Board setup for custom use:
custom_board = Board()
custom_board.grid.grid = [[custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL]]
custom_board.fix_attributes()

Here custom_board.grid.EMPTY_CELL can be swapped for any mark from the custom_board.players list
Then fix_attributes method is run to select which player's turn it is
"""

import copy
from colorama import Fore

from .grid import Grid
from .game_ai import minmax, evaluate
from .state_checker import StateChecker, TTTStateChecker


class Board:
    """Board class for managing the game

    Contains methods for playing a complete tic tac toe game whilst automatically managing
    player turns

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
            Any subclass of ABC StateChecker to check wins or draws and access Win Data
    """

    def __init__(self, size: int = 3, players: list[str] = None, state_checker: StateChecker = None):
        # player_index is zero_indexed variable for indexing players list
        self.player_index: int = 0

        if players is None:
            players = ["X", "O"]
        self.players: list[str] = players

        self.grid: Grid = Grid(size)

        if state_checker is None:
            state_checker = TTTStateChecker(self.grid)
        self.state: StateChecker = state_checker

    def reset(self):
        self.__init__(self.grid.size, self.players, self.state)

    def play_move(self, row: int, column: int, unplay: bool = False):
        """Plays a move on the grid and updates current player
        Uses zero-indexing

        Parameters
        ----------
            row, column : int
                Zero indexed row/column number on which to play the move
            unplay : bool
                If True, play_move marks an Empty cell on the given coordinate i.e. unplays the move
                If False, marks the player whose turn it was on the given coordinate"""

        if not unplay:
            mark = self.get_current_mark()
            self.select_next_player()
        else:
            mark = self.grid.EMPTY_CELL
            self.select_previous_player()

        self.grid.update_cell(row, column, mark)

    def get_current_mark(self) -> str:
        """Get the mark of current player"""
        return self.players[self.player_index]

    def get_previous_mark(self) -> str:
        """Get the mark of the player who played the previous move"""
        return self.players[self.get_previous_index()]

    def get_next_index(self) -> int:
        """Returns index of next player
        Wraps to the starting index (0) when player_index becomes larger than the last player's index"""
        next_player_index = self.player_index + 1
        if next_player_index == len(self.players):
            next_player_index = 0
        return next_player_index

    def get_previous_index(self) -> int:
        """Returns index of previous player
        Wraps to the end index of `self.players` list when player_index becomes smaller than 0"""
        last_player_index = self.player_index - 1
        if last_player_index == -1:
            last_player_index = len(self.players) - 1
        return last_player_index

    def select_next_player(self):
        self.player_index = self.get_next_index()

    def select_previous_player(self):
        self.player_index = self.get_previous_index()

    def fix_player_index(self):
        """Fix player_index to correct player by checking the board state
            Must be run when working with custom setup"""
        raise NotImplementedError("Sorry I was too tired to implement this")

    def ai_play(self):
        """Use the minmax AI function to get the best move and play it"""
        move = minmax(self, maximizing=True, evaluating=False)  # Get best move
        self.play_move(move[0], move[1])


################## CUSTOM SETUP #########################
def evaluate_position(board: Board):
    """Evaluates each legal move and prints it with the grid telling eval of each move"""

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

    # PRINTING STUFF
    eval_grid.print_grid()
    print(f"Player Turn: {board.get_current_mark()}\n")
    print(" 0 - Draw")
    print(f" 1 - {board.players[0]} Wins")
    print(f"-1 - {board.players[1]} Wins")
