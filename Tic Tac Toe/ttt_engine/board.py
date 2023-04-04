# TODO: Implement raising exception when playing a move on an already occupied cell

"""
ttt_engine.board
~~~~~~~~~~~~~~~~

Game Manager/Engine for the playing tic tac toe
The `Board` class controls the player turns, and allows to play the moves on the grid
The Board class also has all the other relavent attributes bundled with it to control other aspects of the game

The gameplay can also be modded, see Modding section of README.md for info

Board setup for custom use:
custom_board = Board()
custom_board.grid.grid = [[custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL],
                         [custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL, custom_board.grid.EMPTY_CELL]]

custom_board.player_index = index_of_whichever_player_turn_do_you_want_it_to_be
                            OR
custom_board.fix_player_index()

Here custom_board.grid.EMPTY_CELL can be swapped for any mark from the custom_board.players list
to start from custom positions

See fix_player_index() method's docs
"""

import copy
from colorama import Fore

from .grid import Grid
from .game_ai import minmax, evaluate
from .state_checker import StateChecker, TTTStateChecker


class Board:
    """Board class for playing the game

    Manages player turns and allows playing of moves
    Also has instances of other important classes such as Grid and StateChecker as attributes to
    provide other functionality such as printing board or checking for wins

    Board class is the main class which should be used to play the games, and its attributes
    should be used to manage various aspects of the game

    Attributes
    ----------
    player_index : int
        Current player index, keeps track of whose turn to move is it
    players : list[str]
        A list of marks which will be used to update the board when a move is played
    grid : Grid
        Instance of Grid class for managing the grid
    state_checker : StateChecker
        Any subclass of ABC StateChecker to check wins or draws and access Win Data

    Methods
    -------
    reset()
        Resets the game to intial state, while keeping game settings like baord size, players and state_checker
    play_move(row, column, unplay)
        Plays/unplays a move on the grid and selects the next player
    fix_player_index()
        Select who's turn to play is it depending upon the number of marks on the grid
    ai_play()
        AI plays a move on the board with selected player and the board selects the next player
    """

    def __init__(self, size: int = 3, players: list[str] = None, state_checker: StateChecker = None):
        """Constructor for Board class

        Parameters
        ----------
        size : int
            Size of the grid, a grid will have `size * size` cells
        players : list[str]
            Player marks which will be used to update board when making a move
        state_checker : StateChecker
            The class used to check if the game is won or drawn, i.e. state of the game
        """

        # player_index is zero_indexed variable for indexing players list
        self.player_index: int = 0

        # If no players are passed, use default players of TTT
        if players is None:
            players = ["X", "O"]
        self.players: list[str] = players

        self.grid: Grid = Grid(size)

        # If no state_checker is passed, use default state checker of TTT
        if state_checker is None:
            state_checker = TTTStateChecker(self.grid)
        self.state_checker: StateChecker = state_checker

    def reset(self):
        """Resets the game to intial state, while keeping game settings like baord size, players and state_checker"""
        self.__init__(self.grid.size, self.players, self.state_checker)

    def play_move(self, row: int, column: int, unplay: bool = False):
        """Plays/unplays a move on the grid and selects the next player

        Parameters
        ----------
            row, column : int
                Zero-indexed row/column numbers of cells to play the move onto
            unplay : bool
                If False, places the current player mark on the cell at row, column
                If True, places an EMPTY_CELL mark on the given coordinate
        """

        if not unplay:
            mark = self.get_current_mark()
            self.select_next_player()
        else:
            mark = self.grid.EMPTY_CELL
            self.select_previous_player()

        self.grid.update_cell(row, column, mark)

    def get_current_mark(self) -> str:
        """Gets the mark of current player"""
        return self.players[self.player_index]

    def get_previous_mark(self) -> str:
        """Gets the mark of the player who played the previous move"""
        return self.players[self.get_previous_index()]

    def get_next_index(self) -> int:
        """Returns index of next player

        Wraps to the starting index (0) when player_index becomes larger than the number of players
        Modulo operator is not used because it felt more implicit to me, this option is more explicit
        """

        next_player_index = self.player_index + 1
        if next_player_index == len(self.players):
            next_player_index = 0
        return next_player_index

    def get_previous_index(self) -> int:
        """Returns index of previous player

        Wraps in a similar way to get_next_index method
        If player_index reaches below 0, wraps to last index of list
        """

        last_player_index = self.player_index - 1
        if last_player_index == -1:
            last_player_index = len(self.players) - 1
        return last_player_index

    def select_next_player(self):
        """Selects next player as the current player, by updating player_index"""
        self.player_index = self.get_next_index()

    def select_previous_player(self):
        """Selects previous player as the current player, by updating player_index"""
        self.player_index = self.get_previous_index()

    def fix_player_index(self):
        """Selects current player depending upon the number of moves made on the grid

        If 7 moves have been made and 2 players are playing, then it must be the turn of the 2nd person to play
        according to this method

        The method ignores the possibility of a player having played multiple moves in a row without other player
        getting a chance when choosing current player
        """

        raise NotImplementedError("Sorry I was too tired to implement this")

    def play_ai_move(self):
        """Use the minmax AI function to get the best move and play it"""
        best_move = minmax(self, maximizing=True, evaluating=False)
        self.play_move(best_move[0], best_move[1])


################## CUSTOM SETUP #########################
# TODO : Remove color coding system, add some prints to tell what +1, -1, 0 indicate for current player
#  Then work on its docs
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
        str_evaluation = str_evaluation.replace("1", "+1")
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
