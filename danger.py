__author__ = 'anosov'


import itertools
from functools import partial

class Type:
    START = 1
    FINISH = 2
    WALL = 3
    LASER = 4
    SPEAR = 5
    BONUS = 6


class Dir:
    # ALL = (0, 1), (1, 0), (0, -1), (-1, 0)
    ALL = (1, 0), (0, 1), (-1, 0), (0, -1)
    UP, RIGHT, DOWN, LEFT = ALL

    @staticmethod
    def move(coord, _dir):
        return tuple(map(sum, zip(coord, _dir)))

    @staticmethod
    def move_generator(coord, _dir):
        while True:
            coord = Dir.move(coord, _dir)
            yield coord


class Danger:
    def __init__(self, coord, _type, periods, dirs=None):
        self.coord = coord
        self.type = _type
        self.on_period = periods[0]
        self.off_period = periods[1]
        self.offset = periods[2]
        self.dirs = dirs                # TODO
        self.danger_cells = list()

    @staticmethod
    def at_stake(period, step):
        on, off, offset = period
        return (step + offset) % (on + off) < on

    @property
    def triple(self):
        return self.on_period, self.off_period, self.offset

    @property
    def quad_dict(self):
        return self.get_period_map()

    @staticmethod
    def at_stake_wrap(period):
        return partial(Danger.at_stake, period)


    def pull(self, time):
        mod = (time + self.offset) % (self.on_period + self.off_period)
        return self.danger_cells if mod < self.on_period else []

    def get_period_map(self):
        on, off = self.on_period, self.off_period
        state = 'on' if self.offset < on else 'off'
        period = self.offset
        if state == 'off':
            period -= on
        return {'onPeriod': on, 'offPeriod': off,
                'currentState': state, 'currentPeriod': period}

    @staticmethod
    def make_all_period(_max=3):
        periods = itertools.product(range(1, _max+1), repeat=2)
        periods = [map(lambda offset: (on, off, offset),
                       xrange(on+off)) for on, off in periods]
        return list(itertools.chain(*periods))