from abc import ABC, abstractmethod

from .grid import Grid
from .state_data import WinType, WinData, GameState


class StateChecker(ABC):
    @property
    @abstractmethod
    def win_data(self):
        """Implement an instance var _win_data and use @property to access it
        .win_data should be accessible publicly"""

    @abstractmethod
    def check_state(self, winner_mark: str, update_win_data: bool = True) -> GameState:
        """Checks if the game is a draw or a win for any player"""

    @abstractmethod
    def check_win(self, winner_mark: str, update_win_data: bool = True) -> GameState:
        """Checks if a player has won the game
        If yes, then updates the win_data if `update_win_data` flag is True"""

    @abstractmethod
    def check_draw(self) -> GameState:
        """Checks if the game is drawn"""


class TTTStateChecker(StateChecker):
    """Class for checking for win or draw using the grid and updating win_data accordingly

    Attributes
    ----------
        grid : Grid
            grid which is used to check the state of the board when methods of TTTStateChecker are called
            to check for win or draw on the board
        _win_data : WinData
            contains win data of the game to manage and update it
            use `self.win_data` property to access `_win_data`

    Methods
    -------
        check_state(other_player: str, update_win_data: bool) -> GameState
            checks if there is a win or draw on the grid or the game is not over
            combines check_win and check_draw together and ensures game state is checked
            the right way, see IMPORTANT to read about "the right way"
        check_win(other_player: str, update_win_data: bool) -> bool
            checks if a player has won on the board using the grid and updates the win_data accordingly
        check_draw() -> bool
            checks if the game is drawn, read its IMPORTANT section for more info
        is_line_winning(line)
            checks if a line (list) contains marks of the same player

    IMPORTANT
    ---------
    For most cases check_state method should be used.

    If check_win and check_draw are called individually then,
    check_win must be called before check_draw while checking the state of the game
    because check_draw just checks if there is no EMPTY_CELL on the grid, and if that happens
    then it returns True but a situation can occur when the board is full and it a victory for a player but
    check_draw is ran before running check_win which caused the developer to declare the game a draw
    even if there was a win on the board
    """

    def __init__(self, grid: Grid):
        self.grid = grid
        self._win_data = WinData()

    @property
    def win_data(self):
        return self._win_data

    def check_state(self, winner_mark: str, update_win_data: bool = True) -> GameState:
        """Checks if there is a win or draw on the grid or the game is not over

        Parameters
        ----------
            winner_mark : str
                mark of the player with whom to update to win data if a victory is detected

            update_win_data : bool
                Flag to update or not update win data if win is detected
                When set to False, does not update the win_data attribute of the state checker
                Useful when working with AI for tic tac toe.

        Returns
        -------
            GameState
                Enum type telling if the game is won, drawn, or is ongoing

        """
        if self.check_win(winner_mark, update_win_data):
            return GameState.WIN
        if self.check_draw():
            return GameState.DRAW
        return GameState.ONGOING

    def check_draw(self) -> bool:
        """Checks for draw on the board

        Returns True if there is no EMPTY_CELL on the board

        IMPORTANT
        ---------
        It does not check if any player has won or not, just checks if all cells are marked
        Which causes it to return True even if a player has won but the board is full,
        so it must be called aftercalling check_win
        A victory is not checked on the board in the check_draw method to avoid calling check_win
        redundantly which will reduce the efficiency of the program as check_win also is a costly function"""

        for row in self.grid.grid:
            if self.grid.EMPTY_CELL in row:
                return False
        return True

    def check_win(self, winner_mark: str, update_win_data: bool = True) -> bool:
        """Checks for win on the board

        Returns True if a player has won the game and updates win_data

        Parameters
        ----------
            update_win_data : bool
                Flag to update win data attribute or not if win occours
            winner_mark : str
                mark of the player with whom to update to win data if a victory is detected
        """

        if self.check_horizontal(update_win_data) or self.check_vertical(update_win_data) \
                or self.check_diagonal(update_win_data):
            if update_win_data:
                self.win_data.winner = winner_mark
            return True

        return False

    def check_horizontal(self, update_win_data: bool = True) -> bool:
        """Checks for horizontal/row wise win and updates win_data"""
        for row_num, row in enumerate(self.grid.grid):

            if self.is_line_winning(row):
                if update_win_data:
                    self.win_data.win_line = [(row_num, column_num) for column_num in range(self.grid.size)]
                    self.win_data.win_type = WinType.HORIZONTAL
                return True

        return False

    def check_vertical(self, update_win_data: bool = True) -> bool:
        """Checks for vertical/column wise win and updates win_data"""
        for column_num in range(self.grid.size):
            column = [self.grid.get_cell(row_num, column_num) for row_num in range(self.grid.size)]

            if self.is_line_winning(column):
                if update_win_data:
                    self.win_data.win_line = [(row_num, column_num) for row_num in range(self.grid.size)]
                    self.win_data.win_type = WinType.VERTICAL
                return True

        return False

    def check_diagonal(self, update_win_data: bool = True) -> bool:
        """Checks for a diagonal win and updates win_data"""
        win_diagonal = None
        grid_size = self.grid.size
        diagonal_1 = [self.grid.get_cell(i, i) for i in range(grid_size)]
        diagonal_2 = [self.grid.get_cell((grid_size - 1) - i, i) for i in range(grid_size)]

        if self.is_line_winning(diagonal_1):
            win_diagonal = [(i, i) for i in range(grid_size)]
        elif self.is_line_winning(diagonal_2):
            win_diagonal = [((grid_size - 1) - i, i) for i in range(grid_size)]

        if not win_diagonal:
            return False

        if update_win_data:
            self.win_data.win_line = win_diagonal
            self.win_data.win_type = WinType.DIAGONAL

        return True

    @staticmethod
    def is_line_winning(line: list[str]) -> bool:
        """Checks if all the cells in a line are of same player and not empty"""

        first_mark = line[0]
        if first_mark == Grid.EMPTY_CELL:
            return False

        for mark in line[1:]:
            if mark != first_mark:
                return False
        return True
