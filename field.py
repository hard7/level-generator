__author__ = 'anosov'

from danger import Type, Dir, Danger
import string
import copy
from itertools import repeat
import numpy
from collections import deque
import json
import pprint


class Field:
    def __init__(self, x, y):
        self._dim_x, self._dim_y = x, y
        self._danger_cells = []
        self._danger_objects = []
        self._blocker_cells = []
        self._start = None
        self._finish = None
        self._time = None
        self._backup_dict = None
        self.stars = []

        self.free_cells = []
        for i in xrange(x):
            for j in xrange(y):
                self.free_cells.append((i, j))


    def add_object(self, coord, type_, periods=None, dirs=None):
        self.free_cells.remove(coord)
        if type_ == Type.HERO:
            self._start = coord
        elif type_ == Type.FINISH:
            self._finish = coord
        elif type_ == Type.BRICK:
            self._blocker_cells.append(coord)
        elif type_ == Type.SPEAR:
            danger = Danger(coord, type_, periods)
            self._danger_objects.append(danger)
        elif type_ == Type.LASER:
            danger = Danger(coord, type_, periods, dirs)
            self._danger_objects.append(danger)
            self._blocker_cells.append(coord)
        elif type_ == Type.STAR:
            self.stars.append(coord)

    def brick_to_laser(self, coord, periods, dirs):
        danger = Danger(coord, Type.LASER, periods, dirs)
        self._danger_objects.append(danger)

    def laser_to_brick(self, coord):
        for danger in self._danger_objects:
            if danger.coord == coord:
                self._danger_objects.remove(danger)
                self.init()
                break


    def get_free_cells(self):
        all = [(i, j) for i in xrange(self._dim_x) for j in xrange(self._dim_y)]
        print all

    def add_group(self, coords, *args, **kwargs):
        for c in coords:
            self.add_object(c, *args, **kwargs)

    def save_backup(self):
        self._backup_dict = copy.deepcopy(self.__dict__)

    def load_backup(self):
        assert self._backup_dict is not None
        self.__dict__ = self._backup_dict
        self.save_backup()

    get_start = lambda self: self._start
    get_finish = lambda self: self._finish

    def set_time(self, time):
        if self._time == time:
            return

        self._time = time
        self._danger_cells = []
        for danger in self._danger_objects:
            self._danger_cells.extend(danger.pull(time))

    dim = property(lambda self: (self._dim_x, self._dim_y))

    def available_cells(self, coord):
        blocker = self._blocker_cells
        danger = self._danger_cells
        result = []
        for dir_ in Dir.ALL:
            ofs = Dir.move(coord, dir_)
            if self._in_range(ofs) and ofs not in blocker and ofs not in danger:
                result.append(ofs)
        return result

    def _in_range(self, coord):
        x, y = coord
        return (0 <= x < self._dim_x) and (0 <= y < self._dim_y)

    def init(self):
        for danger in self._danger_objects:
            danger.danger_cells = []
            if danger.type == Type.SPEAR:
                danger.danger_cells.append(danger.coord)

            elif danger.type == Type.LASER:
                for dir_ in danger.dirs:
                    coord = danger.coord
                    while not self._is_blocker(Dir.move(coord, dir_)):
                        coord = Dir.move(coord, dir_)
                        danger.danger_cells.append(coord)

    def is_valid(self):
        self.set_time(0)
        return self._start not in self._danger_cells

    def _is_blocker(self, coord):
        return coord in self._blocker_cells or not self._in_range(coord)

    def take_text(self, name='x'):
        prop = json.loads(self.take_json())
        msg = str()
        # msg += '\n'
        # msg += '%s\n' % prop['name']
        # msg += '%i %i\n' % tuple(prop['size'])
        msg += '\n'.join(prop['map'])
        # msg += '%i\n' % len(prop['symbols'])

        disq = 'EMPTY WALL HERO FINISH BONUS'.split()
        if any([p['type'] not in disq for p in prop['symbols']]):
            msg += '\n\n'
            vars = 'symbol type currentState onPeriod ' \
                   'offPeriod currentPeriod dangerousSide'
            for symbol in prop['symbols']:
                p = [symbol.get(v, '') for v in vars.split()]
                not_disq = symbol['type'] not in disq
                msg += ' '.join(map(str, p)) + '\n' if not_disq else ''

        return msg

    def take_json(self, name='noname'):
        alphabet = deque(string.ascii_uppercase)
        dx, dy = self._dim_x, self._dim_y
        level = dict()
        level['name'] = name
        level['size'] = [dx, dy]
        level['map'] = ['NOT IMPLEMENTED']
        level['symbols'] = None

        symbols = list()
        symbols.append({'symbol': '.', 'type': 'EMPTY'})
        symbols.append({'symbol': '#', 'type': 'WALL'})
        symbols.append({'symbol': 'o', 'type': 'HERO'})
        symbols.append({'symbol': '^', 'type': 'FINISH'})
        symbols.append({'symbol': '+', 'type': 'BONUS'})

        def set_symbol((x, y), symbol):
            art[y][x] = symbol

        get_symbol = lambda (x, y): art[y][x]

        art = [['.']*dx for _ in xrange(dy)]
        set_symbol(self._start, 'o')
        set_symbol(self._finish, '^')
        [set_symbol(c, '#') for c in self._blocker_cells]
        [set_symbol(c, '+') for c in self.stars]

        for dang in self._danger_objects:
            prop = dang.get_period()
            if dang.type == Type.LASER:
                set_symbol(dang.coord, alphabet.popleft())
                prop['symbol'] = get_symbol(dang.coord)
                prop['type'] = 'LASER'
                prop['dangerousSide'] = \
                    [d in dang.dirs for d in Dir.ALL]
            if dang.type == Type.SPEAR:
                set_symbol(dang.coord, alphabet.pop())
                prop['symbol'] = get_symbol(dang.coord)
                prop['type'] = 'SPEAR'
            symbols.append(prop)
        level['map'] = map(''.join, art[::-1])
        level['symbols'] = symbols

        return json.dumps(level, indent=2, sort_keys=True)

if __name__ == '__main__':
    field = Field(8, 5)
    field.add_object((2, 3), Type.HERO)
    field.add_object((2, 2), Type.BRICK)
    field.add_object((1, 1), Type.LASER, (1, 1, 1), [Dir.UP])

    field.init()
    field.set_time(0)
    print field.available_cells(field.get_start())