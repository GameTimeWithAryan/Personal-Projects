from board import Board


BOARD_SIZE = 3
AI_MODE = 0


def console_game():
    print("Input format:")
    print("<row> <column>\n")

    game_board = Board(3)
    game_board.grid.print_grid()

    while True:
        if game_board.check_win():
            print(game_board.win_manager.winner, "WON")
            break
        elif game_board.check_draw():
            print("DRAW")
            break

        move = input("Enter move - ")
        if move == "ai":
            game_board.ai_play()
            game_board.grid.print_grid()
        else:
            row, column = map(int, move.split(" "))
            is_move_played = game_board.play_move(row - 1, column - 1)

            if is_move_played:
                game_board.grid.print_grid()
                continue
            if AI_MODE:
                game_board.ai_play()
                game_board.grid.print_grid()


if __name__ == '__main__':
    console_game()
