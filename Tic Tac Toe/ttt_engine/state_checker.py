from .win_data import WinType, WinData
from .grid import Grid


class StateChecker:
    """Class for checking for win or draw using the grid and updating win_data accordingly
    This class checks for win or draw and also updates the win_data

    Attributes
    ----------
        grid : Grid
            grid which is used to check the state of the board when methods of StateChecker are called
            to check for win or draw on the board
        win_data : WinData
            passed for updating the win_data of the board whenever a win occurs

    Methods
    -------
        check_win(other_player: str) -> bool
            checks if a player has won on the board using the grid and updates the win_data accordingly
        check_draw() -> bool
            checks if the game is drawn

    IMPORTANT
    ---------
    check_win must be called before check_draw while checking the state of the game
    else a situation can occur when the board is full and it a victory for a player but check_draw gives True
    """

    def __init__(self, grid: Grid, win_data: WinData):
        self.grid = grid
        self.win_data = win_data

    def check_draw(self) -> bool:
        """Checks for draw on the board
        Returns True if all the cells are marked in the grid

        IMPORTANT
        ---------
        check_draw will return True if the grid is full even when a player has won on the last move
        because it will not check if a player has already won or not"""
        for row in self.grid.grid:
            if Grid.EMPTY_CELL in row:
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
