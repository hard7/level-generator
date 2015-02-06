import random_coord


class Generator(object):
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.cell_count = x_coord * y_coord
        r = random_coord.UniqueRandomCoord
        self.random_coord = r(x_coord, y_coord)

    def make_field(self, prop=None):
        msg = 'Method Generator.make_field is pure virtual'
        raise NotImplementedError(msg)
