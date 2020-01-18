import sys

import pygame

from Tetris.Colors import RED, WHITE, BLACK, GREY
from Tetris.Grid import valid_shape_coordinates, create, clear_rows, check_lost
from Tetris.Piece import get_piece_coordinate, get_piece
from Tetris.Shapes import get_random_shape

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300    # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600   # meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT


def get_label(text, size, color=WHITE, bold=False):
    f = pygame.font.SysFont('comicsans', size, bold=bold)
    return f.render(text, 1, color)


def draw_grid(s, row, col):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(row):
        i1 = (sx, sy + i * BLOCK_SIZE)
        i2 = (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE)
        pygame.draw.line(s, GREY, i1, i2)  # horizontal lines
        for j in range(col):
            j1 = (sx + j * BLOCK_SIZE, sy)
            j2 = (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT)
            pygame.draw.line(s, GREY, j1, j2)  # vertical lines


def draw_window(s, g, score=0 ):
    s.fill(BLACK)

    # Tetris Title
    label = get_label('TETRIS', 60)

    s.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), BLOCK_SIZE))

    for i in range(len(g)):
        for j in range(len(g[i])):
            dimension = (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(s, g[i][j], dimension, 0)

    # draw grid and border
    draw_grid(s, 20, 10)
    pygame.draw.rect(s, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    # score
    label = get_label('Score ' + str(score), BLOCK_SIZE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100

    s.blit(label, (sx + 20, sy + 160))


def draw_next_shape(shape, surface):
    label = get_label('Next Shape', BLOCK_SIZE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100

    shape_mode = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_mode):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - BLOCK_SIZE))


def draw_text_middle(text, size, color, surface):
    label = get_label(text, size, color, bold=True)
    w = TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2)
    h = TOP_LEFT_Y + PLAY_HEIGHT / 2 - (label.get_height() / 2)
    surface.blit(label, (w, h))


def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create(locked_positions)

    change_piece = False
    run = True
    current_piece = get_piece()
    next_piece = get_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    while run:
        fall_speed = 0.27

        grid = create(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_shape_coordinates(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_shape_coordinates(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_shape_coordinates(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_shape_coordinates(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_shape_coordinates(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = get_piece_coordinate(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_piece()
            change_piece = False

            # call four times to check for multiple clear rows
            score += clear_rows(grid, locked_positions) * 10

        draw_window(window, grid, score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, WHITE, window)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        window.fill(BLACK)
        draw_text_middle('Press any key to begin.', 60, WHITE, window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()
    sys.exit()


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

main_menu()
