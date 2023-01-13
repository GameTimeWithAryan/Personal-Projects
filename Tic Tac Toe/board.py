import copy
from math import inf
from colorama import Fore

# Board setup for custom use
# game_board = Board()
# game_board.board = [[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
#                     [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
#                     [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]]
# game_board.player_index = 0  # set player index to whose turn it is, 0 means first player, 1 means second player

EMPTY_CELL = "_"


class Board:
    def __init__(self):
        self.board = [[EMPTY_CELL for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.player_index = 0

        self.has_moved = False
        self.winner = None
        self.win_line = []
        self.win_type = ''

    def reset(self):
        self.__init__()

    def print_board(self, board: list = None):
        if board is None:
            board = self.board
        print()
        print("<-ROW->")
        print("  1 2 3")
        for row in range(3):
            print(f'{row + 1} {" ".join(board[row])}')
        print()

    def play_move(self, row: int, column: int):
        if self.is_empty(row, column):
            self.has_moved = True
            self.board[column - 1][row - 1] = self.get_player()
            self.switch_player()
            return True
        else:
            return False

    def check_win(self):
        if self.check_horizontal(self.board) or self.check_vertical(self.board) or self.check_diagonal(self.board):
            self.switch_player()
            self.winner = self.get_player()
            return True
        return False

    def check_draw(self):
        for col in self.board:
            if EMPTY_CELL in col:
                return False
        return True

    def is_empty(self, row: int, column: int):
        return self.board[column - 1][row - 1] == EMPTY_CELL

    def get_cell(self, row: int, column: int):
        return self.board[column - 1][row - 1]

    def get_player(self):
        return self.players[self.player_index]

    def switch_player(self):
        self.player_index = int(not self.player_index)

    def get_legal_moves(self):
        legal_moves = []
        for col_num, col in enumerate(self.board):
            for row_num, cell in enumerate(col):
                if cell == EMPTY_CELL:
                    legal_moves.append((row_num + 1, col_num + 1))
        return legal_moves

    def check_horizontal(self, board):
        for col_num, column in enumerate(board):
            if is_line_equal(column):
                self.win_line = [(row_num + 1, col_num + 1) for row_num in range(3)]
                self.win_type = "horizontal"
                return True
        return False

    def check_vertical(self, board):
        for row_num in range(3):
            column = [board[column_num][row_num] for column_num in range(3)]
            if is_line_equal(column):
                self.win_line = [(row_num + 1, column_num + 1) for column_num in range(3)]
                self.win_type = "vertical"
                return True
        return False

    def check_diagonal(self, board):
        diagonal_1 = [board[i][i] for i in range(3)]
        diagonal_2 = [board[i][2 - i] for i in range(3)]

        if is_line_equal(diagonal_1):
            self.win_line = [(i + 1, i + 1) for i in range(3)]
            self.win_type = "diagonal"
            return True
        elif is_line_equal(diagonal_2):
            self.win_line = [(i + 1, 2 - i + 1) for i in range(3)]
            return True
        return False

    def ai_play(self):
        move = minmax(self, True, False)
        if move:
            self.play_move(move[0], move[1])


def is_line_equal(line: list):
    check_item = line[0]
    if check_item == EMPTY_CELL:
        return False
    for item in line[1:]:
        if item != check_item:
            return False
    return True


##################### AI ###########################

def unplay_move(board: Board, row: int, column: int):
    board.board[column - 1][row - 1] = EMPTY_CELL
    board.switch_player()


def minmax(minmax_board: Board, maximizing: bool, evaluating=True):
    min_eval = inf
    max_eval = -inf
    best_move = None
    board_copy = copy.deepcopy(minmax_board)

    if board_copy.check_win():
        return -1 if maximizing else 1
    if board_copy.check_draw():
        return 0

    for move in board_copy.get_legal_moves():
        evaluation = evaluate(board_copy, move, not maximizing)
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


def evaluate(board, move, maximizing):
    board.play_move(move[0], move[1])
    evaluation = minmax(board, maximizing)
    unplay_move(board, move[0], move[1])
    return evaluation


def evaluate_position(board: Board):
    evaluations = []
    eval_color_coding = {"0": Fore.BLUE, "1": Fore.GREEN, "-1": Fore.RED} if board.player_index == 0 \
        else {"0": Fore.BLUE, "1": Fore.RED, "-1": Fore.GREEN}

    for move in board.get_legal_moves():
        evaluation = str(evaluate(board, move, bool(board.player_index)))
        evaluation = eval_color_coding[evaluation] + evaluation + "\033[0m"
        evaluations.append(evaluation)

    board_board = board.board
    for idx, place in enumerate(board.get_legal_moves()):
        board_board[place[1] - 1][place[0] - 1] = evaluations[idx]

    board.print_board(board_board)
    print(f"Player Turn: {board.get_player()}")


def main():
    b = Board()
    b.board = [[EMPTY_CELL, "X", EMPTY_CELL],
               [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
               [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]]
    b.player_index = 1
    evaluate_position(b)


if __name__ == '__main__':
    main()
