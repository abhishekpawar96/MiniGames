import numpy as np

ROW_COUNT = 6
COL_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT,COL_COUNT))

def drop_piece(b, r, c, p):
    b[r][c] = p

def is_valid_location(b, c):
    return b[ROW_COUNT-1][c] == 0

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


board = create_board()
game_over = False
turn = 0
1
print_board(board)

while not game_over:
    # Ask Player 1
    if turn == 0:
        col = int(input("Player 1's selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            if winning_move(board, 1):
                print("Player 1 Wins")
                game_over = True
                break

    # Ask Player 2
    else:
        col = int(input("Player 2's selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                print("Player 2 Wins")
                game_over = True
                break

    print_board(board)

    turn += 1
    turn %= 2