import math
import numpy as np
import pygame
import sys

ROW_COUNT = 6
COL_COUNT = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)


def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT))


def drop_piece(b, r, c, p):
    b[r][c] = p


def is_valid_location(b, c):
    return b[ROW_COUNT - 1][c] == 0


def get_next_open_row(b, c):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def print_board(b):
    print(np.flip(b, 0))


def winning_move(b, p):
    # Check horizontal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if b[r][c] == p \
                    and b[r][c + 1] == p \
                    and b[r][c + 2] == p \
                    and b[r][c + 3] == p:
                return True

    # Check vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == p \
                    and b[r + 1][c] == p \
                    and b[r + 2][c] == p \
                    and b[r + 3][c] == p:
                return True

    # Check +ve Slope
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == p \
                    and b[r + 1][c + 1] == p \
                    and b[r + 2][c + 2] == p \
                    and b[r + 3][c + 3] == p:
                return True

    # Check -ve Slope
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if b[r][c] == p \
                    and b[r - 1][c + 1] == p \
                    and b[r - 2][c + 2] == p \
                    and b[r - 3][c + 3] == p:
                return True


def draw_row_0():
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))


def draw_circle(c, p):
    pygame.draw.circle(screen, c, p, RADIUS)


def draw_board(b):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            w = c * SQUARE_SIZE
            h = r * SQUARE_SIZE + SQUARE_SIZE
            p = int(c * SQUARE_SIZE + SQUARE_SIZE / 2)
            o = int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)
            dimensions = (w, h, SQUARE_SIZE, SQUARE_SIZE)
            position = (p, o)
            pygame.draw.rect(screen, BLUE, dimensions)
            draw_circle(BLACK, position)

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            p = int(c * SQUARE_SIZE + SQUARE_SIZE / 2)
            o = height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)
            position = (p, o)
            if b[r][c] == 1:
                draw_circle(RED, position)
            elif b[r][c] == 2:
                draw_circle(YELLOW, position)

    pygame.display.update()


def player_move(b, p, t):
    if t == 0:
        player = 1
        color = RED
    else:
        player = 2
        color = YELLOW
    c = int(math.floor(p / SQUARE_SIZE))
    if is_valid_location(b, c):
        r = get_next_open_row(b, c)
        drop_piece(b, r, c, player)
        if winning_move(b, player):
            screen.blit(label_font.render("Player {} Wins!!".format(player), player, color), (40, 10))
            print("Player {} Wins!!".format(player))
            return True
        else:
            return False
    else:
        return False


board = create_board()

game_over = False
turn = 0

pygame.init()
label_font = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(size)
print_board(board)
draw_board(board)
pygame.display.update()


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            draw_row_0()
            center = (event.pos[0], int(SQUARE_SIZE / 2))
            if turn == 0:
                draw_circle(RED, center)
            else:
                draw_circle(YELLOW, center)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_row_0()
            game_over = player_move(board, event.pos[0], turn)

            draw_board(board)
            print_board(board)

            turn += 1
            turn %= 2

            if game_over:
                pygame.time.wait(3000)
