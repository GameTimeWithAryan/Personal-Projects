from board import Board


def console_game():
    print("Input format:")
    print("<row> <column>\n")

    game_board = Board()
    game_board.print_board()
    ai_mode = 1

    while True:
        if game_board.check_win():
            print(game_board.winner, "WON")
            break
        elif game_board.check_draw():
            print("DRAW")
            break

        move = input("Enter move - ").strip()
        if "ai" in move:
            game_board.ai_play()
            game_board.print_board()
        else:
            column, row = map(int, move.split(" "))
            is_move_played = game_board.play_move(row, column)
            if is_move_played:
                game_board.print_board()
                if ai_mode:
                    game_board.ai_play()
                    game_board.print_board()


if __name__ == '__main__':
    console_game()
