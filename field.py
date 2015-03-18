__author__ = 'anosov'

from danger import Type, Dir, Danger
import string
import copy
from itertools import product, takewhile
from collections import deque
from functools import partial
import json

class Field:
    def __init__(self, dim):
        self.dim = dim
        self._danger_cells = []
        self._danger_objects = []
        self._blocker_cells = []
        self.bricks = []
        self._start = None
        self._finish = None
        self._time = None
        self._backup_dict = None
        self.stars = []

        self.free_cells = \
            list(product(*map(xrange, dim)))

    # def solve(self):
    #     return solver.Solver(self).run()

    def add_object(self, coord, type_, periods=None, dirs=None):
        self.free_cells.remove(coord)
        if type_ == Type.START:
            self._start = coord
        elif type_ == Type.FINISH:
            self._finish = coord
        elif type_ == Type.BRICK:
            self._blocker_cells.append(coord)
            self.bricks.append(coord)
        elif type_ == Type.SPEAR:
            danger = Danger(coord, type_, periods)
            self._danger_objects.append(danger)
        elif type_ == Type.LASER:
            danger = Danger(coord, type_, periods, dirs)
            self._danger_objects.append(danger)
            self._blocker_cells.append(coord)
        elif type_ == Type.BONUS:
            self.stars.append(coord)

    def brick_to_laser(self, coord, periods, dirs):
        self.bricks.remove(coord)
        danger = Danger(coord, Type.LASER, periods, dirs)
        self._danger_objects.append(danger)
        self.init()

    def laser_to_brick(self, coord):
        self.bricks.append(coord)
        is_equal_coord = lambda d: d.coord == coord
        dan = next(filter(is_equal_coord, self._danger_objects))
        self._danger_objects.remove(dan)

    def add_group(self, coords, *args, **kwargs):
        for c in coords:
            self.add_object(c, *args, **kwargs)

    def save_backup(self):
        self.__dict__['_backup_dict'] = None
        self._backup_dict = copy.deepcopy(self.__dict__)

    def load_backup(self):
        assert self._backup_dict is not None
        self.__dict__ = self._backup_dict
        self.save_backup()

    start = property(lambda self: self._start)
    finish = property(lambda self: self._finish)

    def set_time(self, time):
        if self._time == time:
            return

        self._time = time
        self._danger_cells = []
        for danger in self._danger_objects:
            self._danger_cells.extend(danger.pull(time))

    def available_for_move(self, coord):
        bad_cells = self._blocker_cells + self._danger_cells
        for_check = map(partial(Dir.move, coord), Dir.ALL)
        check = lambda c: self._in_range(c) and c not in bad_cells
        return filter(check, for_check)

    def _in_range(self, coord):
        dx, dy = self.dim
        x, y = coord
        return 0 <= x < dx and 0 <= y < dy

    def init(self):
        is_empty = lambda c: not self._is_blocker(c)

        def init_danger(d):
            if d.type == Type.SPEAR:
                d.danger_cells.append(d.coord)
            elif d.type == Type.LASER:
                for _dir in d.dirs:
                    gen = Dir.move_generator(d.coord, _dir)
                    r = takewhile(is_empty, gen)
                    d.danger_cells.extend(list(r))
        map(init_danger, self._danger_objects)

    def is_valid(self):
        self.set_time(0)
        return self.start not in self._danger_cells

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

        disq = 'EMPTY WALL START FINISH BONUS'.split()
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
        dx, dy = self.dim
        level = dict()
        level['name'] = name
        level['size'] = [dx, dy]
        level['map'] = ['NOT IMPLEMENTED']
        level['symbols'] = None

        symbols = list()
        symbols.append({'symbol': '.', 'type': 'EMPTY'})
        symbols.append({'symbol': '#', 'type': 'WALL'})
        symbols.append({'symbol': 'o', 'type': 'START'})
        symbols.append({'symbol': '^', 'type': 'FINISH'})
        symbols.append({'symbol': '+', 'type': 'BONUS'})

        def set_symbol((x, y), symbol):
            art[y][x] = symbol

        get_symbol = lambda (x, y): art[y][x]

        art = [['.']*dx for _ in xrange(dy)]
        set_symbol(self.start, 'o')
        set_symbol(self.finish, '^')
        [set_symbol(c, '#') for c in self._blocker_cells]
        [set_symbol(c, '+') for c in self.stars]

        for dang in self._danger_objects:
            prop = dang.get_period_map()
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
    field.add_object((2, 3), Type.START)
    field.add_object((2, 2), Type.BRICK)
    field.add_object((1, 1), Type.LASER, (1, 1, 1), [Dir.UP])

    field.init()
    field.set_time(0)
    print field.available_for_move(field.start)