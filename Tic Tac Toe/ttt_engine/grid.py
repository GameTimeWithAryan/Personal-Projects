"""
ttt_engine.grid
~~~~~~~~~~~~~~~

Grid for keeping track of moves played

Grid class remembers the moves played, and provides methods to get info about cells on the grid
"""

from typing import TypeAlias

# Coordinate defining the position of cell on the board
# i.e. Index in the 2D grid list
Coordinate: TypeAlias = tuple[int, int]


class Grid:
    """Grid class for managing the grid of the game

    Allows updating cells, checking mark of a cell, priting the grid
    and getting all the legal moves

    Attributes
    ----------
    EMPTY_CELL : str
        mark of the empty cell to be used while creating the grid and checking empty cells
    size : str
        size of the grid, a grid (2D list) will be generated of size * size dimensions
    grid : list[list[str]]
        the actual grid storing the cells

    Methods
    -------
    is_empty(row, column)
        Checks if cell at a coordinate is empty
    get_cell(row, column)
        Gets the mark of cell at row, column
    update_cell(row, column, mark)
        Updates cell of a grid at row, column with mark
    get_legal_moves()
        Gets all legal moves on the grid
    print_grid()
        Prints the grid
    """

    EMPTY_CELL = "_"

    def __init__(self, size: int):
        """Generates a new grid of dimensions size * size"""
        self.size: int = size
        self.grid: list[list[str]] = [[Grid.EMPTY_CELL for _ in range(size)] for _ in range(size)]

    def is_empty(self, row: int, column: int) -> bool:
        """Returns True if mark at (row, column) is an empty cell mark, else returns False"""
        return self.get_cell(row, column) == Grid.EMPTY_CELL

    def get_cell(self, row: int, column: int) -> str:
        """Gets the mark of cell at (row, column)"""
        return self.grid[row][column]

    def update_cell(self, row: int, column: int, mark: str):
        """Updates the value of the cell at (row, column) with mark"""
        self.grid[row][column] = mark

    def get_legal_moves(self) -> list[Coordinate]:
        """Returns a list of coordinates (row, column) of all Empty Cells

        Examples
        --------
        Let the grid be:

          1 2 3
        1 _ X O
        2 X O _
        3 X X O

        then get_legal_moves() method will return [(0,0), (1, 2)]
        """

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
