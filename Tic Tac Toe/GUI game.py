"""
This file does not follow SOLID principles or any good coding techniques
"""

import pygame
from ttt_engine import Board, WinType, GameState

# Game variables
BOARD_SIZE = 3
GAME_MODE = 1  # 0 for Single Player, 1 for AI
AI_PLAYER = 1  # player index, [0, 1]


class Button:
    def __init__(self, text: str, size: tuple[int, int], position: tuple[float, float], colors: tuple[str, str]):
        self.is_pressed = False

        self.primary_color = colors[0]
        self.hover_color = colors[1]
        self.color = self.primary_color

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = position

        self.text_surf = text_font.render(text, True, "white")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def handle_mouse(self):
        global game_over
        global has_moved
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            self.color = self.hover_color

            if pygame.mouse.get_pressed()[0]:
                self.is_pressed = True
            else:
                if self.is_pressed:
                    game_board.reset()
                    game_over = False
                    has_moved = False
                    self.is_pressed = False
        else:
            self.color = self.primary_color

    def update(self):
        self.draw()
        self.handle_mouse()


def get_mark_color():
    return "#FF615F" if game_board.get_current_mark() == game_board.players[1] else "#3EC5F3"


def is_mouse_on_board(mouse_position: tuple[int, int]):
    return board_x_pos < mouse_position[0] < board_x_pos + board_size \
        and board_y_pos < mouse_position[1] < board_y_pos + board_size


def get_row_column_from_mouse(mouse_position: tuple[int, int]):
    if not is_mouse_on_board(mouse_position):
        return None, None
    mouse_x, mouse_y = mouse_position
    row_num = (mouse_y - board_y_pos) // (board_size // 3)
    column_num = (mouse_x - board_x_pos) // (board_size // 3)
    return row_num, column_num


def draw_grid():
    # Draw Board Lines
    for i in range(1, 3):
        # Vertical Lines
        line_x_pos = board_x_pos + i * board_size / 3  # x position will be changing when drawing vertically
        pygame.draw.line(screen, black_bg_color, (line_x_pos, board_y_pos), (line_x_pos, board_y_pos + board_size), 6)

        # Horizontal Lines
        line_y_pos = board_y_pos + i * board_size / 3  # y position will be changing when drawing horizontally
        pygame.draw.line(screen, black_bg_color, (board_x_pos, line_y_pos), (board_x_pos + board_size, line_y_pos), 6)


def draw_marks():
    # Draw marked marks on board
    for row_num in range(1, 4):
        for column_num in range(1, 4):
            cell = game_board.grid.get_cell(row_num - 1, column_num - 1)
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
    if not game_board.state_checker.win_data.win_line:
        return

    adjustment = 45
    x_adjustment = 0
    y_adjustment = 0

    make_one_indexed = lambda x: (x[0] + 1, x[1] + 1)
    win_start_row, win_start_column = make_one_indexed(game_board.state_checker.win_data.win_line[0])
    win_end_row, win_end_column = make_one_indexed(game_board.state_checker.win_data.win_line[2])

    line_start_x = board_x_pos + win_start_column * board_size / 3 - board_size / 6
    line_end_x = board_x_pos + win_end_column * board_size / 3 - board_size / 6

    line_start_y = board_y_pos + win_start_row * board_size / 3 - board_size / 6
    line_end_y = board_y_pos + win_end_row * board_size / 3 - board_size / 6

    line_color = get_mark_color()

    if game_board.state_checker.win_data.win_type == WinType.HORIZONTAL:
        x_adjustment = adjustment
    elif game_board.state_checker.win_data.win_type == WinType.VERTICAL:
        y_adjustment = adjustment
    elif game_board.state_checker.win_data.win_type == WinType.DIAGONAL:
        if game_board.state_checker.win_data.win_line == [(i, i) for i in range(game_board.grid.size)]:
            x_adjustment = y_adjustment = adjustment
        else:
            x_adjustment = adjustment
            y_adjustment = -adjustment

    line_start_x -= x_adjustment
    line_end_x += x_adjustment

    line_start_y -= y_adjustment
    line_end_y += y_adjustment

    pygame.draw.line(screen, line_color, (line_start_x, line_start_y), (line_end_x, line_end_y), 15)


def draw_text(text: str, text_bg_rectange: pygame.Rect, colors: tuple[str, str]):
    """
    colors[0] -> Text background color
    colors[1] -> Text color
    """

    text_surface = text_font.render(text, True, colors[1])
    text_rectangle = text_surface.get_rect(center=text_bg_rectange.center)

    pygame.draw.rect(screen, colors[0], text_bg_rectange)
    screen.blit(text_surface, text_rectangle)


# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 700  # 8:7 is recommended ratio for resolution
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)

game_board = Board(BOARD_SIZE)

game_over = False
has_moved = False
green_bg_color = "#14bdac"
black_bg_color = "#3b3b3b"
foreground_color = "white"
title = ""

# Making Board
board_size = 390
board_x_pos = (WIDTH - board_size) // 2
board_y_pos = (HEIGHT - board_size) // 2
board_rect = pygame.Rect(board_x_pos, board_y_pos, board_size, board_size)

# Title
title_bg_rect = pygame.Rect((0, 0), (200, 75))
title_bg_rect.center = (WIDTH / 2, (HEIGHT - board_size) / 4)

# Reset button
reset_button = Button("Reset", (200, 55),
                      (WIDTH / 2, (HEIGHT - (HEIGHT - board_size) / 4)),
                      ("#3b3b3b", "#030303"))

# AI Event
ai_trigger_event = pygame.USEREVENT + 1
if GAME_MODE == 1:
    pygame.time.set_timer(ai_trigger_event, 100)

while True:
    if not game_over:
        # Updating Title
        game_state = game_board.state_checker.check_state(game_board.get_previous_mark())
        if game_state == GameState.WIN:
            title = f"Winner: {game_board.state_checker.win_data.winner}"
            game_over = True
        elif game_state == GameState.DRAW:
            title = "Draw"
            game_over = True
        else:
            title = game_board.get_current_mark()

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Check if player clicked
        if event.type == pygame.MOUSEBUTTONUP and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            row, column = get_row_column_from_mouse(mouse_pos)
            # row, column will be None, None if the mouse_click did not occur on the board
            if row is None:
                continue

            # If clicked on board, play move
            if game_board.grid.is_empty(row, column):
                game_board.play_move(row, column)
                has_moved = True

        if event.type == ai_trigger_event and not game_over and game_board.player_index == AI_PLAYER:
            game_board.play_ai_move()

    # Drawing everything
    screen.fill(green_bg_color)
    pygame.draw.rect(screen, foreground_color, board_rect)
    draw_grid()
    draw_marks()
    draw_win_line()

    # Reset Button
    if has_moved:
        reset_button.update()

    # Title
    draw_text(title, title_bg_rect, (black_bg_color, foreground_color))

    pygame.display.update()
    clock.tick(60)
