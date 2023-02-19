import copy
from math import inf
from colorama import Fore

from grid import Grid
from win_manager import WinType, WinManager


# Board setup for custom use
# custom_board = Board()
# custom_board.board = [[Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
#                       [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
#                       [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL]]
# custom_board.fix_attributes()


class Board:

    def __init__(self, size: int = 3):
        self.player_index: int = 0
        self.players: list[str] = ["X", "O"]

        self.grid: Grid = Grid(size)
        self.win_manager = WinManager()

    def reset(self):
        self.__init__(self.grid.size)

    def play_move(self, row: int, column: int) -> bool:
        if not self.grid.is_empty(row, column):
            return False

        self.grid.update_cell(self.get_current_player(), row, column)
        self.grid.update_has_moved()
        self.switch_player()
        return True

    def unplay_move(self, row: int, column: int) -> bool:
        if self.grid.is_empty(row, column):
            return False

        self.grid.update_cell(Grid.EMPTY_CELL, row, column)
        self.grid.update_has_moved()
        self.switch_player()
        return True

    def check_win(self) -> bool:
        if self.check_horizontal() or self.check_vertical() or self.check_diagonal():
            self.win_manager.winner = self.players[self.get_other_player_index()]
            return True
        return False

    def check_draw(self) -> bool:
        for row in self.grid.grid:
            if Grid.EMPTY_CELL in row:
                return False
        return True

    def check_horizontal(self) -> bool:
        for row_num, row in enumerate(self.grid.grid):

            if not self.grid.is_line_equal(row):
                continue

            self.win_manager.win_line = [(row_num, column_num) for column_num in range(self.grid.size)]
            self.win_manager.win_type = WinType.HORIZONTAL
            return True
        return False

    def check_vertical(self) -> bool:
        for column_num in range(self.grid.size):
            column = [self.grid.get_cell(row_num, column_num) for row_num in range(self.grid.size)]

            if not self.grid.is_line_equal(column):
                continue

            self.win_manager.win_line = [(row_num, column_num) for row_num in range(self.grid.size)]
            self.win_manager.win_type = WinType.VERTICAL
            return True
        return False

    def check_diagonal(self) -> bool:
        win_diagonal = None
        grid_size = self.grid.size
        diagonal_1 = [self.grid.get_cell(i, i) for i in range(grid_size)]
        diagonal_2 = [self.grid.get_cell((grid_size - 1) - i, i) for i in range(grid_size)]

        if self.grid.is_line_equal(diagonal_1):
            win_diagonal = [(i, i) for i in range(grid_size)]

        elif self.grid.is_line_equal(diagonal_2):
            win_diagonal = [((grid_size - 1) - i, i) for i in range(grid_size)]

        if not win_diagonal:
            return False

        self.win_manager.win_line = win_diagonal
        self.win_manager.win_type = WinType.DIAGONAL
        return True

    def get_current_player(self) -> str:
        return self.players[self.player_index]

    def get_other_player_index(self) -> int:
        return int(not self.player_index)

    def switch_player(self):
        self.player_index = self.get_other_player_index()

    def fix_attributes(self):
        """ Manually fix/assign attributes of the class by checking the board state
            Must be run when working with custom setup """

        self.grid.update_has_moved()

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
        eval_grid.update_cell(str_evaluations[index], row, column)

    # PRINTING
    eval_grid.print_grid()
    print(f"Player Turn: {board.get_current_player()}\n")
    print(" 0 - Draw")
    print(f" 1 - {board.players[0]} Wins")
    print(f"-1 - {board.players[1]} Wins")


############# MAIN #############
def main():
    board = Board(3)
    board.grid.print_grid()


if __name__ == '__main__':
    main()
