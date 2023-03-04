from ttt_engine import Board

game_board = Board(3)


def get_move() -> str | tuple[int, int]:
    while True:
        move = input("Enter move - ")
        if move == "ai":
            break

        try:
            row, column = map(int, move.split(" "))
            move = (row - 1, column - 1)
        except ValueError:
            print("Enter row and column number only")
            continue

        if game_board.grid.is_empty(row - 1, column - 1):
            break
        print(f"({row}, {column}) is not empty")

    return move


def play_move(move: str | tuple[int, int]):
    if move == "ai":
        game_board.ai_play()
        return

    row, column = move
    game_board.play_move(row, column)


def select_game_mode():
    AI_PLAYER = 1

    AI_MODE = int(input("Do you want to play with AI? [0 for No | 1 for Yes] - "))
    if AI_MODE == 1:
        AI_PLAYER = int(input("Should AI play the first move or you? [0 for AI | 1 for Yourself] - "))

    return AI_MODE, AI_PLAYER


def console_game():
    AI_MODE, AI_PLAYER = select_game_mode()
    print("Input format:")
    print("<row> <column>\n")
    game_board.grid.print_grid()

    while True:

        if AI_MODE == 1 and AI_PLAYER == 0:
            game_board.ai_play()
            game_board.grid.print_grid()

        if game_board.state.check_win(game_board.get_other_player()):
            print(game_board.state.win_data.winner, "WON")
            break

        elif game_board.state.check_draw():
            print("DRAW")
            break

        move = get_move()
        play_move(move)
        game_board.grid.print_grid()

        if AI_MODE == 1 and AI_PLAYER == 1:
            game_board.ai_play()
            game_board.grid.print_grid()


if __name__ == '__main__':
    console_game()
