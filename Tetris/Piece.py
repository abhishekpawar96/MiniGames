from Tetris.Shapes import SHAPES, get_random_shape
from Tetris.Colors import COLORS

rows = 20  # y
columns = 10  # x


class Piece(object):

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0


def get_piece():
    return Piece(5, 0, get_random_shape())


def get_piece_coordinate(p):
    coordinates = []
    shape_mode = p.shape[p.rotation % len(p.shape)]

    for i, line in enumerate(shape_mode):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                coordinates.append((p.x + j, p.y + i))

    for i, c in enumerate(coordinates):
        coordinates[i] = (c[0] - 2, c[1] - 4)

    return coordinates

