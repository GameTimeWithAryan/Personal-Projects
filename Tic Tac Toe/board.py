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


class Board:
    EMPTY_CELL = "_"

    def __init__(self):
        self.board = [[Board.EMPTY_CELL for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.player_index = 0

        self.moves_played = 0
        self.winner = None
        self.win_line = []
        self.win_type = ''

    def reset(self):
        self.__init__()

    def print_board(self, board: list = None):
        if board is None:
            board = self.board
        print()
        print("  1 2 3")
        for row in range(3):
            print(f'{row + 1} {" ".join(board[row])}')
        print()

    def play_move(self, row: int, column: int):
        if self.is_empty(row, column):
            self.board[row][column] = self.get_player()
            self.switch_player()
            self.moves_played += 1
            return True
        return False

    def unplay_move(self, row: int, column: int):
        if not self.is_empty(row, column):
            self.board[row][column] = Board.EMPTY_CELL
            self.switch_player()
            self.moves_played -= 1
            return True
        return False

    def check_win(self):
        if self.check_horizontal(self.board) or self.check_vertical(self.board) or self.check_diagonal(self.board):
            self.winner = self.players[self.get_other_player()]
            return True
        return False

    def check_draw(self):
        for row in self.board:
            if Board.EMPTY_CELL in row:
                return False
        return True

    def get_legal_moves(self):
        legal_moves = []
        for row_num, row in enumerate(self.board):
            for column_num, cell in enumerate(row):
                if cell == Board.EMPTY_CELL:
                    legal_moves.append((row_num, column_num))
        return legal_moves

    def check_horizontal(self, board: list):
        for row_num, row in enumerate(board):
            if self.is_line_equal(row):
                self.win_line = [(row_num, column_num) for column_num in range(3)]
                self.win_type = WinType.HORIZONTAL
                return True
        return False

    def check_vertical(self, board: list):
        for column_num in range(3):
            column = [board[row_num][column_num] for row_num in range(3)]
            if self.is_line_equal(column):
                self.win_line = [(row_num, column_num) for row_num in range(3)]
                self.win_type = WinType.VERTICAL
                return True
        return False

    def check_diagonal(self, board):
        diagonal_1 = [board[i][i] for i in range(3)]
        diagonal_2 = [board[i][2 - i] for i in range(3)]

        if self.is_line_equal(diagonal_1):
            self.win_line = [(i, i) for i in range(3)]
            self.win_type = WinType.DIAGONAL
            return True
        elif Board.is_line_equal(diagonal_2):
            self.win_line = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def is_empty(self, row: int, column: int):
        return self.board[row][column] == Board.EMPTY_CELL

    def get_cell(self, row: int, column: int):
        return self.board[row][column]

    def get_player(self):
        return self.players[self.player_index]

    def get_other_player(self):
        return int(not self.player_index)

    def switch_player(self):
        self.player_index = self.get_other_player()

    @staticmethod
    def is_line_equal(line: list):
        check_item = line[0]
        if check_item == Board.EMPTY_CELL:
            return False
        for item in line[1:]:
            if item != check_item:
                return False
        return True

    def fix_attributes(self):
        """ Manually fix/assign attributes of the class by checking the board state
            Useful when working with custom setup """

        self.moves_played = len(self.get_legal_moves())

        if self.moves_played % 2 == 1:
            self.player_index = 0
        else:
            self.player_index = 1

    def ai_play(self):
        minmax_board = copy.deepcopy(self)
        move = minmax(minmax_board, True, False)
        if move:
            self.play_move(move[0], move[1])


##################### AI ###########################

def minmax(minmax_board: Board, maximizing: bool, evaluating: bool = True):
    min_eval = inf
    max_eval = -inf
    best_move = None

    if minmax_board.check_win():
        return -1 if maximizing else 1
    if minmax_board.check_draw():
        return 0

    for move in minmax_board.get_legal_moves():
        evaluation = evaluate(minmax_board, move, not maximizing)
        if maximizing:
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            if evaluation == 1:
                return max_eval if evaluating else best_move
        elif not maximizing:
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            if evaluation == -1:
                return min_eval if evaluating else best_move

    if evaluating:
        return max_eval if maximizing else min_eval
    return best_move


def evaluate(board: Board, move: tuple, maximizing: bool):
    board.play_move(move[0], move[1])
    evaluation = minmax(board, maximizing)
    board.unplay_move(move[0], move[1])
    return evaluation


################## CUSTOM SETUP #########################
def evaluate_position(board: Board):
    board.fix_attributes()

    str_evaluations = []
    legal_moves = board.get_legal_moves()
    eval_color_coding = {"0": Fore.BLUE, "1": Fore.GREEN, "-1": Fore.RED} if board.player_index == 0 \
        else {"0": Fore.BLUE, "1": Fore.RED, "-1": Fore.GREEN}

    for move in legal_moves:
        str_evaluation = str(evaluate(board, move, bool(board.player_index)))
        str_evaluation = eval_color_coding[str_evaluation] + str_evaluation + Fore.RESET
        str_evaluations.append(str_evaluation)

    eval_board = board.board
    for index, (row, column) in enumerate(legal_moves):
        eval_board[row][column] = str_evaluations[index]

    # PRINTING
    board.print_board(eval_board)
    print(f"Player Turn: {board.get_player()}\n")
    print("0 - Draw")
    print("1 - Player 1 Wins")
    print("2 - Player 2 Wins")


############# MAIN #############
def main():
    custom_board = Board()
    custom_board.board = [["X", Board.EMPTY_CELL, Board.EMPTY_CELL],
                          [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL],
                          [Board.EMPTY_CELL, Board.EMPTY_CELL, Board.EMPTY_CELL]]
    evaluate_position(custom_board)


if __name__ == '__main__':
    main()
