"""
Main Module for using the tic tac toe engine
Contains Board class to control the board and play the game

Usage
-----
Defining a board:
game_board = Board(3)

Board setup for custom use:
custom_board = Board(3)
custom_board.grid.grid = [[custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL]]
custom_board.fix_attributes()

Here custom_board.EMPTY_CELL can be swapped for any mark from the custom_board.players list
Then fix_attributes method is run to select which player's turn it is
"""

import copy
from colorama import Fore

from .grid import Grid
from .state_checker import StateChecker
from .minmax import minmax, evaluate


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
        Uses zero-indexing

        Parameters
        ----------
            row, column : int
                Zero indexed row/column number on which to play the move
            unplay : bool
                If True, play_move marks an Empty cell on the given coordinate i.e. unplays the move
                If False, marks the player whose turn it was on the given coordinate"""

        mark = self.get_current_player()
        if unplay:
            mark = self.grid.EMPTY_CELL

        self.grid.update_cell(row, column, mark)
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
        self.play_move(move[0], move[1])


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
