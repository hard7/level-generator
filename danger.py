__author__ = 'anosov'


class Type:
    HERO = 1
    FINISH = 2
    BRICK = 3
    LASER = 4
    SPEAR = 5


class Dir:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)
    ALL = [LEFT, RIGHT, UP, DOWN]

    @staticmethod
    def move(coord, dir_):
        return tuple((coord[0]+dir_[0], coord[1]+dir_[1]))


class Danger:
    def __init__(self, coord, type_, periods, dirs=None):
        self.coord = coord
        self.type = type_
        self.on_period = periods[0]
        self.off_period = periods[1]
        self.offset = periods[2]
        self.dirs = dirs                # TODO
        self.danger_cells = []

    def pull(self, time):
        mod = (time + self.offset) % (self.on_period + self.off_period)
        cond = mod < self.on_period
        return self.danger_cells if cond else []