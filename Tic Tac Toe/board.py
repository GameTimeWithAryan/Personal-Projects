import copy
from math import inf
from colorama import Fore
from enum import Enum, auto


# Board setup for custom use
# custom_board = Board()
# custom_board.board = [[Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
#                       [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
#                       [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL]]


class WinType(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


class Grid:
    def __init__(self, size: int):
        """Generates a new grid of size, size * size"""
        self.grid: list[list[str]] = [[Board.EMPTY_CELL for _ in range(size)] for _ in range(size)]
        self.size: int = size

    def get_cell(self, row: int, column: int) -> str:
        return self.grid[row][column]

    def make_move(self, mark: str, row: int, column: int):
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
                if cell == Board.EMPTY_CELL:
                    legal_moves.append((row_num, column_num))
        return legal_moves

    def is_empty(self, row: int, column: int) -> bool:
        return self.grid[row][column] == Board.EMPTY_CELL

    @staticmethod
    def is_line_equal(line: list) -> bool:
        check_item = line[0]
        if check_item == Board.EMPTY_CELL:
            return False
        for item in line[1:]:
            if item != check_item:
                return False
        return True


class Board:
    EMPTY_CELL = "_"

    def __init__(self, grid: Grid):
        self.grid: Grid = grid

        self.player_index: int = 0
        self.players: list[str] = ["X", "O"]
        self.has_moved: bool = False

        self.winner: str | None = None
        self.win_line: list[str] = []
        self.win_type: WinType | None = None

    def reset(self):
        new_grid = Grid(size=self.grid.size)
        self.__init__(new_grid)

    def play_move(self, row: int, column: int) -> bool:
        if self.grid.is_empty(row, column):
            self.grid.make_move(self.get_current_player(), row, column)
            self.update_has_moved()
            self.switch_player()
            return True
        return False

    def unplay_move(self, row: int, column: int) -> bool:
        if not self.grid.is_empty(row, column):
            self.grid.make_move(Board.EMPTY_CELL, row, column)
            self.update_has_moved()
            self.switch_player()
            return True
        return False

    def check_win(self) -> bool:
        if self.check_horizontal() or self.check_vertical() or self.check_diagonal():
            self.winner = self.players[self.get_other_player_index()]
            return True
        return False

    def check_draw(self) -> bool:
        for row in self.grid.grid:
            if Board.EMPTY_CELL in row:
                return False
        return True

    def check_horizontal(self) -> bool:
        grid_size = self.grid.size
        for row_num, row in enumerate(self.grid.grid):
            if self.grid.is_line_equal(row):
                self.grid.win_line = [(row_num, column_num) for column_num in range(grid_size)]
                self.grid.win_type = WinType.HORIZONTAL
                return True
        return False

    def check_vertical(self) -> bool:
        grid_size = self.grid.size
        for column_num in range(grid_size):
            column = [self.grid.grid[row_num][column_num] for row_num in range(grid_size)]
            if self.grid.is_line_equal(column):
                self.grid.win_line = [(row_num, column_num) for row_num in range(grid_size)]
                self.grid.win_type = WinType.VERTICAL
                return True
        return False

    def check_diagonal(self) -> bool:
        grid_size = self.grid.size
        diagonal_1 = [self.grid.grid[i][i] for i in range(grid_size)]
        diagonal_2 = [self.grid.grid[i][(grid_size - 1) - i] for i in range(grid_size)]

        if self.grid.is_line_equal(diagonal_1):
            self.grid.win_line = [(i, i) for i in range(grid_size)]
            self.grid.win_type = WinType.DIAGONAL
            return True
        elif self.grid.is_line_equal(diagonal_2):
            self.grid.win_line = [(i, (grid_size - 1) - i) for i in range(grid_size)]
            self.grid.win_type = WinType.DIAGONAL
            return True
        return False

    def get_current_player(self) -> str:
        return self.players[self.player_index]

    def get_other_player_index(self) -> int:
        return int(not self.player_index)

    def switch_player(self):
        self.player_index = self.get_other_player_index()

    def update_has_moved(self):
        legal_moves = self.grid.get_legal_moves()
        self.has_moved = len(legal_moves) != self.grid.size ** 2

    def fix_attributes(self):
        """ Manually fix/assign attributes of the class by checking the board state
            Must be run when working with custom setup """

        self.update_has_moved()

        if len(self.grid.get_legal_moves()) % 2 == 1:
            self.player_index = 0
        else:
            self.player_index = 1

    def ai_play(self):
        minmax_board = copy.deepcopy(self)
        move = minmax(minmax_board)  # Get best move
        if move:
            self.play_move(move[0], move[1])


##################### AI ###########################

def minmax(minmax_board: Board, maximizing: bool = True, evaluating: bool = False):
    """ Minmax AI for Tic Tac Toe
        maximizing: Maximizing or the Minimizing player in minmax algorithm
        evaluating: When evaluating is True, returns the best evaluation of player
                    When evaluating is False, returns the best move on the board """
    min_eval = inf
    max_eval = -inf
    best_move: tuple[int, int] | None = None

    if minmax_board.check_win():
        return -1 if maximizing else 1
    if minmax_board.check_draw():
        return 0

    for move in minmax_board.grid.get_legal_moves():
        evaluation = evaluate(minmax_board, move, not maximizing)
        if maximizing:
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
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


def evaluate(board: Board, move: tuple[int, int], maximizing: bool):
    board.play_move(move[0], move[1])
    evaluation = minmax(board, maximizing=maximizing, evaluating=True)
    board.unplay_move(move[0], move[1])
    return evaluation


################## CUSTOM SETUP #########################
def evaluate_position(board: Board):
    board.fix_attributes()
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
        eval_grid.grid[row][column] = str_evaluations[index]

    # PRINTING
    eval_grid.print_grid()
    print(f"Player Turn: {board.get_current_player()}\n")
    print(" 0 - Draw")
    print(f" 1 - {board.players[0]} Wins")
    print(f"-1 - {board.players[1]} Wins")


############# MAIN #############
def main():
    board_grid = Grid(3)
    custom_board = Board(board_grid)
    custom_board.grid.grid = [["X", Board.EMPTY_CELL, "O"],
                              [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
                              [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL]]
    evaluate_position(custom_board)


if __name__ == '__main__':
    main()
