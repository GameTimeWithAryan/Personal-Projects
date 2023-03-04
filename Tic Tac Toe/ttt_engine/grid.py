"""
Modules containing class for managing grid system in Tic Tac Toe
Contains class Grid

Each horizontal straight line is a row
Each vertical straight line is column

So "X" mark at (2, 3) would be row 2 and column 3 i.e.
  1 2 3
1 _ _ _
2 _ _ X
3 _ _ _

An empty grid is a list of list, having rows as a list of 3 cells and 3 rows in a grid:
[ [ Board.EMPTY_CELL , Board.EMPTY_CELL , Board.EMPTY_CELL ] ,
  [ Board.EMPTY_CELL , Board.EMPTY_CELL , Board.EMPTY_CELL ] ,
  [ Board.EMPTY_CELL , Board.EMPTY_CELL , Board.EMPTY_CELL ] ]
"""

from typing import TypeAlias

# Coordinate defining the position of cell on the board
Coordinate: TypeAlias = tuple[int, int]


class Grid:
    """
    Class for managing the grid of tic-tac-toe

    Contains methods to control the board of tic tac toe, by updating cells
    and other helper functions like is_empty and get_cell

        Attributes
        ----------
            EMPTY_CELL : str
                value of empty cell to be used while creating the grid and checking empty cells
            size : str
                size used to generate the grid, dimensions of grid will be size * size
            has_moved : bool
                Tells if any player has played a move
                Needs to be updated manually everytime board state changes by calling update_has_moved()
                Can be used for GUI games for rendering reset buttons only when a player has moved
            grid : list[list[str]]
                the grid for storing cells and making moves

        Methods
        -------
            is_empty(row, column)
                checks if cell at (row, column) is empty
            get_cell(row, column)
                gets value of cell at row, column
            update_cell(row, column, mark)
                updates cell of a grid at row, column
            get_legal_moves()
                gets all legal moves on the board
            print_grid()
                prints the grid
            update_has_moved()
                updates has_moved attribute
            is_line_winning(line)
                checks if a line (list) contains marks of the same player
    """

    EMPTY_CELL = "_"

    def __init__(self, size: int):
        """Generates a new grid of size, size * size"""
        self.size: int = size
        self.has_moved: bool = False

        # Generates a grid list
        self.grid: list[list[str]] = [[Grid.EMPTY_CELL for _ in range(size)] for _ in range(size)]

    def is_empty(self, row: int, column: int) -> bool:
        """Returns True if value at (row, column) is an Empty cell else returns False"""
        return self.get_cell(row, column) == Grid.EMPTY_CELL

    def get_cell(self, row: int, column: int) -> str:
        """Gets the value of cell at (row, column)"""
        return self.grid[row][column]

    def update_cell(self, row: int, column: int, mark: str):
        """Updates the value of the cell at (row, column) with new mark"""
        self.grid[row][column] = mark

    def get_legal_moves(self) -> list[Coordinate]:
        """Returns a list of coordinates (row, column) of all Empty Cells

            Example
            --------
                let the grid be:

                  1 2 3
                1 _ X O
                2 X O _
                3 X X O

                then get_legal_moves() method will return [(1,1), (2, 3)]"""

        legal_moves = []
        for row_num, row in enumerate(self.grid):
            for column_num, cell in enumerate(row):
                if cell == Grid.EMPTY_CELL:
                    legal_moves.append((row_num, column_num))
        return legal_moves

    def print_grid(self):
        """Prints the grid"""
        # generates column labels above grid
        # column_label for size 3 -> "1 2 3"
        column_label = " ".join([str(num + 1) for num in range(self.size)])

        print()
        print(f"  {column_label}")
        for index, row in enumerate(self.grid):
            print(f'{index + 1} {" ".join(row)}')
        print()

    def update_has_moved(self):
        """Checks number of moves made on board to update has_moved

        NOTE
        ----
        Needs to be called everytime board state changes to update has_moved attribute"""

        legal_moves = self.get_legal_moves()
        self.has_moved = len(legal_moves) != self.size ** 2

    @staticmethod
    def is_line_winning(line: list[str]) -> bool:
        """Checks if all the cells in a line are of same player and not empty,

            A line of cells can be passed to check if they create a win condition which means a
            player has won the game"""

        first_mark = line[0]
        if first_mark == Grid.EMPTY_CELL:
            return False

        for mark in line[1:]:
            if mark != first_mark:
                return False
        return True
