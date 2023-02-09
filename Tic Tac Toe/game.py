"""
This file does not follow SOLID principles or any good coding techniques
"""

import pygame
from board import Board, WinType


class ResetButton:
    def __init__(self, text: str, size, position):
        self.pressed = False

        self.top_color = "#3b3b3b"
        self.top_rect = pygame.Rect((0, 0), size)
        self.top_rect.center = position

        self.text_surf = text_font.render(text, True, "white")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def handle_mouse(self):
        global game_over
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = "#030303"

            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    game_board.reset()
                    game_over = False
                    self.pressed = False
        else:
            self.top_color = "#3b3b3b"

    def update(self):
        self.draw()
        self.handle_mouse()


def get_mark_color():
    return "#FF615F" if game_board.get_current_player() == game_board.players[1] else "#3EC5F3"


def mouse_on_board(mouse_position):
    return board_x_pos < mouse_position[0] < board_x_pos + board_size and board_y_pos < mouse_position[
        1] < board_y_pos + board_size


def get_row_column_from_mouse(mouse_position):
    # Run only if `mouse_on_board(mouse_position)` is True
    mouse_x, mouse_y = mouse_position
    row_num = (mouse_y - board_y_pos) // 130
    column_num = (mouse_x - board_x_pos) // 130
    return row_num, column_num


def draw_grid():
    # Draw Board Lines
    for i in range(1, 3):
        # Vertical Lines
        line_x_pos = board_x_pos + i * board_size / 3  # x position will be changing when drawing vertically
        pygame.draw.line(screen, secondary_color, (line_x_pos, board_y_pos), (line_x_pos, board_y_pos + board_size), 6)

        # Horizontal Lines
        line_y_pos = board_y_pos + i * board_size / 3  # y position will be changing when drawing horizontally
        pygame.draw.line(screen, secondary_color, (board_x_pos, line_y_pos), (board_x_pos + board_size, line_y_pos), 6)


def draw_marks():
    # Draw marked marks on board
    for row_num in range(1, 4):
        for column_num in range(1, 4):
            cell = game_board.get_cell(row_num - 1, column_num - 1)
            mark_pos_x = board_x_pos + board_size * column_num / 3 - board_size / 6
            mark_pos_y = board_y_pos + board_size * row_num / 3 - board_size / 6
            if cell == "X":
                mark_surf = pygame.image.load('marks/cross.png').convert_alpha()
                mark_rect = mark_surf.get_rect(center=(mark_pos_x, mark_pos_y))
            elif cell == "O":
                mark_surf = pygame.image.load('marks/circle.png').convert_alpha()
                mark_rect = mark_surf.get_rect(center=(mark_pos_x, mark_pos_y))
            else:
                continue
            screen.blit(mark_surf, mark_rect)


def draw_win_line():
    # Draw line connecting winning marks
    if not game_board.win_line:
        return

    adjustment = 45
    x_adjustment = 0
    y_adjustment = 0
    increment_1 = lambda x: (x[0] + 1, x[1] + 1)
    win_start_row, win_start_column = increment_1(game_board.win_line[0])
    win_end_row, win_end_column = increment_1(game_board.win_line[2])

    line_start_x = board_x_pos + win_start_column * board_size / 3 - board_size / 6  # Lift all four values more
    line_start_y = board_y_pos + win_start_row * board_size / 3 - board_size / 6
    line_end_x = board_x_pos + win_end_column * board_size / 3 - board_size / 6
    line_end_y = board_y_pos + win_end_row * board_size / 3 - board_size / 6

    line_color = get_mark_color()

    if game_board.win_type == WinType.HORIZONTAL:
        x_adjustment = adjustment

    if game_board.win_type == WinType.VERTICAL:
        y_adjustment = adjustment

    if game_board.win_type == WinType.DIAGONAL:
        x_adjustment = y_adjustment = adjustment

    line_start_x -= x_adjustment
    line_end_x += x_adjustment
    line_start_y -= y_adjustment
    line_end_y += y_adjustment

    pygame.draw.line(screen, line_color, (line_start_x, line_start_y), (line_end_x, line_end_y), 15)


# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)

# Game variables
# AI
GAME_MODE = 1  # 0 for Single Player, 1 for AI
AI_PLAYER = 1  # player index, [0, 1]

game_board = Board()

game_over = False
primary_color = "#14bdac"
accent_color = "white"
secondary_color = "#3b3b3b"
title = ""

# Making Board
board_size = 390
board_x_pos = (WIDTH - board_size) // 2
board_y_pos = (HEIGHT - board_size) // 2
board_rect = pygame.Rect(board_x_pos, board_y_pos, board_size, board_size)

# Title
title_bg_rect = pygame.Rect(0, 0, 200, 75)
title_bg_rect.center = (WIDTH / 2, (HEIGHT - board_size) / 4)

# Reset button
reset_button = ResetButton("Reset", (200, 55), (WIDTH / 2, (HEIGHT - (HEIGHT - board_size) / 4)))
ai_trigger_event = pygame.USEREVENT + 1
if GAME_MODE == 1:
    pygame.time.set_timer(ai_trigger_event, 100)

while True:
    if not game_over:
        if game_board.check_win():
            title = f"Winner: {game_board.winner}"
            game_over = True
        elif game_board.check_draw():
            title = "Draw"
            game_over = True
        else:
            title = game_board.get_current_player()

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONUP and not game_over and mouse_on_board(mouse_pos := pygame.mouse.get_pos()):
            row, column = get_row_column_from_mouse(mouse_pos)
            game_board.play_move(row, column)

        if event.type == ai_trigger_event:
            if game_board.player_index == AI_PLAYER and not game_over:
                game_board.ai_play()

    # Drawing everything
    screen.fill(primary_color)
    pygame.draw.rect(screen, accent_color, board_rect)
    draw_grid()
    draw_marks()
    draw_win_line()

    # Reset Button
    if game_board.moves_played:
        reset_button.update()

    # Title
    pygame.draw.rect(screen, secondary_color, title_bg_rect)
    title_surf = text_font.render(title, True, accent_color)
    title_rect = title_surf.get_rect(center=title_bg_rect.center)
    screen.blit(title_surf, title_rect)

    pygame.display.update()
    clock.tick(60)
