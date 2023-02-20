class Grid:
    EMPTY_CELL = "_"

    def __init__(self, size: int):
        """Generates a new grid of size, size * size"""
        self.has_moved: bool = False
        self.grid: list[list[str]] = [[Grid.EMPTY_CELL for _ in range(size)] for _ in range(size)]
        self.size: int = size

    def get_cell(self, row: int, column: int) -> str:
        return self.grid[row][column]

    def update_cell(self, mark: str, row: int, column: int):
        self.grid[row][column] = mark

    def print_grid(self):
        column_label = " ".join([str(column_num + 1) for column_num in range(self.size)])
        print()
        print(f"  {column_label}")
        for index, row in enumerate(self.grid):
            print(f'{index + 1} {" ".join(row)}')
        print()

    def get_legal_moves(self) -> list[tuple[int, int]]:
        legal_moves = []
        for row_num, row in enumerate(self.grid):
            for column_num, cell in enumerate(row):
                if cell == Grid.EMPTY_CELL:
                    legal_moves.append((row_num, column_num))
        return legal_moves

    def update_has_moved(self):
        legal_moves = self.get_legal_moves()
        self.has_moved = len(legal_moves) != self.size ** 2

    def is_empty(self, row: int, column: int) -> bool:
        return self.get_cell(row, column) == Grid.EMPTY_CELL

    @staticmethod
    def is_line_equal(line: list) -> bool:
        check_item = line[0]
        if check_item == Grid.EMPTY_CELL:
            return False
        for item in line[1:]:
            if item != check_item:
                return False
        return True
