from Tetris.Colors import BLACK
from Tetris.Piece import get_piece_coordinate


def create(locked_coordinates=None):
    if locked_coordinates is None:
        locked_coordinates = {}

    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_coordinates:
                c = locked_coordinates[(j, i)]
                grid[i][j] = c
    return grid


def valid_shape_coordinates(s, g):
    accepted_coordinates = [[(j, i) for j in range(10) if g[i][j] == BLACK] for i in range(20)]
    flatten = []
    for inner_list in accepted_coordinates:
        for j in inner_list:
            flatten.append(j)

    coordinates = get_piece_coordinate(s)

    for c in coordinates:
        if c not in flatten:
            if c[1] > -1:
                return False

    return True


def check_lost(coordinates):
    for c in coordinates:
        x, y = c
        if y < 1:
            return True
    return False


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    global ind
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc
