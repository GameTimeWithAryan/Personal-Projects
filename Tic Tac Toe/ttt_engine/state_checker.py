from .state_data import WinType, WinData, GameState
from .grid import Grid


class StateChecker:
    """Class for checking for win or draw using the grid and updating win_data accordingly

    Attributes
    ----------
        grid : Grid
            grid which is used to check the state of the board when methods of StateChecker are called
            to check for win or draw on the board
        win_data : WinData
            contains win data of the game to manage and update it

    Methods
    -------
        check_state(other_player: str) -> GamesState
            checks if there is a win or draw on the grid or the game is not over
            combines check_win and check_draw together and ensures game state is checked
            the right way, see IMPORTANT to read about "the right way"
        check_win(other_player: str) -> bool
            checks if a player has won on the board using the grid and updates the win_data accordingly
        check_draw() -> bool
            checks if the game is drawn

    IMPORTANT
    ---------
    check_win must be called before check_draw while checking the state of the game
    because check_draw just checks if there is no EMPTY_CELL on the grid, and if that happens
    then it returns True but a situation can occur when the board is full and it a victory for a player but
    check_draw is ran before running check_win which caused the developer to declare the game a draw
    even if there was a win on the board
    """

    def __init__(self, grid: Grid):
        self.grid = grid
        self.win_data = WinData()

    def check_state(self, other_player: str) -> GameState:
        """Checks if there is a win or draw on the grid or the game is not over

        Parameters
        ----------
        other_player : str
            Mark of the player other than whose turn it is to move
            board.get_other_player() returns the expected parameter
            where board is an instance of Board class

        Returns
        -------
        GameState
            Enum type telling if the game is won, drawn, or is ongoing

        """
        if self.check_win(other_player):
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

    def check_win(self, other_player: str) -> bool:
        """Checks for win on the board

        Returns True if a player has won the game and updates win_data

        Parameters
        ----------
            other_player : str
                mark of the player other than whose turn it is to move
                i.e. the player who played the last move
        """

        if self.check_horizontal() or self.check_vertical() or self.check_diagonal():
            self.win_data.winner = other_player
            return True
        return False

    def check_horizontal(self) -> bool:
        """Checks for horizontal/row wise win and updates win_data"""
        for row_num, row in enumerate(self.grid.grid):

            if self.grid.is_line_winning(row):
                self.win_data.win_line = [(row_num, column_num) for column_num in range(self.grid.size)]
                self.win_data.win_type = WinType.HORIZONTAL
                return True

        return False

    def check_vertical(self) -> bool:
        """Checks for vertical/column wise win and updates win_data"""
        for column_num in range(self.grid.size):
            column = [self.grid.get_cell(row_num, column_num) for row_num in range(self.grid.size)]

            if self.grid.is_line_winning(column):
                self.win_data.win_line = [(row_num, column_num) for row_num in range(self.grid.size)]
                self.win_data.win_type = WinType.VERTICAL
                return True

        return False

    def check_diagonal(self) -> bool:
        """Checks for a diagonal win and updates win_data"""
        win_diagonal = None
        grid_size = self.grid.size
        diagonal_1 = [self.grid.get_cell(i, i) for i in range(grid_size)]
        diagonal_2 = [self.grid.get_cell((grid_size - 1) - i, i) for i in range(grid_size)]

        if self.grid.is_line_winning(diagonal_1):
            win_diagonal = [(i, i) for i in range(grid_size)]

        elif self.grid.is_line_winning(diagonal_2):
            win_diagonal = [((grid_size - 1) - i, i) for i in range(grid_size)]

        if not win_diagonal:
            return False

        self.win_data.win_line = win_diagonal
        self.win_data.win_type = WinType.DIAGONAL
        return True
