__author__ = 'anosov'

from danger import Type, Dir, Danger
import string
import copy
from itertools import product, takewhile, compress
from collections import deque
from functools import partial
import json
import utils


interface = '''
cell_type:
    SPEAR, LASER, BONUS, START, FINISH, WALL, (TIME)
    PIT, PLATFORM, KEY, DOOR, EMPTY, PORTAL

cell:
    _danger_sources = []
    set_coord(coord)
    get_coord() -> coord
    get_type() -> coord.type
    is_blocked() -> bool
    is_safely(step) -> bool

periodic:
    get_set_enable() -> int
    get_set_disable() -> int
    get_set_offset() -> int
    get_set_period() -> tuple3
    is_enable/disable(step) -> bool

directed:
    get_directs() -> directly.direct

tagged:
    get_tag() -> string

spear(cell, periodic)
laser(cell, periodic, directed):
    rays
bonus(cell)
key(cell, tagged)
door(cell, tagged)
pit(cell)
time(cell)  <- [bad feature]
empty(cell)
wall(cell)
start(cell)
finish(cell)
platform(cell)
portal(cell, tagged)

Field
    _laser_locations = []
    set_cell(Cell)
    type_cell_in_coord(coord) -> cell.type
    type_cell_in_coord_equal(coord, _type) -> bool
    set_cell_in_coord(cell, coord)

    load_from_json(File)
    save_to_json(File)
    is_safely(coord, step) -> bool

maybe_hang = bonus, key, finish, portal
always_hang = pit, platform
always_stand = start, spear, floor
always_on_hill = laser, door, hill


x_field.add(Spear, (1, 2), (3, 2, 1), Start, (1, 2), Finish, (1, 2), HANG)
x_field.add(Spear((1, 2), (3, 1, 1)))




'''


class Field(object):
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

    @staticmethod
    def load_by_json(_file):
        if isinstance(_file, str):
            with open(_file) as f:
                return Field.load_by_json(f)

        assert isinstance(_file, file)
        symbols = dict()
        level = json.load(_file, encoding='utf-8')
        for s in level['symbols']:
            name = s['symbol']
            symbols[name] = s
            del symbols[name]['symbol']

        f = Field(level['size'][::-1])
        _map = level['map'][::-1]
        for y, x in product(*map(xrange, f.dim)):
            s = symbols[_map[y][x]]
            if s['type'] == 'START': f.add_object((y, x), Type.START)
            elif s['type'] == 'FINISH': f.add_object((y, x), Type.FINISH)
            elif s['type'] == 'WALL': f.add_object((y, x), Type.WALL)
            elif s['type'] == 'BONUS': f.add_object((y, x), Type.BONUS)
            elif s['type'] == 'SPEAR':
                on = s['onPeriod']
                off = s['offPeriod']
                is_off = s['currentState'] == 'off'
                period = s['currentPeriod'] + is_off * on
                f.add_spear((y, x, on, off, period))
            elif s['type'] == 'LASER':
                on = s['onPeriod']
                off = s['offPeriod']
                is_off = s['currentState'] == 'off'
                period = s['currentPeriod'] + is_off * on
                dir = compress(Dir.ALL, s['dangerousSide'])
                f.add_object((y, x), Type.LASER, (on, off, period, dir))
        return f

    def get_danger_by_coord(self, *args):
        coord = args[0] if len(args) == 1 else args[:2]
        _dict = {d_obj.coord: d_obj for d_obj in self._danger_objects}
        return _dict[coord]

    def get_spear_coords(self):
        is_spear = lambda d: d.type == Type.SPEAR
        return [dc.coord for dc in self._danger_objects if is_spear(dc)]

    def add_object(self, coord, type_, periods=None, dirs=None):
        self.free_cells.remove(coord)
        if type_ == Type.START:
            self._start = coord
        elif type_ == Type.FINISH:
            self._finish = coord
        elif type_ == Type.WALL:
            self._blocker_cells.append(coord)
            self.bricks.append(coord)
        elif type_ == Type.SPEAR:
            self.add_spear(coord + periods)
            # danger = Danger(coord, type_, periods)
            # self._danger_objects.append(danger)
        elif type_ == Type.LASER:
            danger = Danger(coord, type_, periods, dirs)
            self._danger_objects.append(danger)
            self._blocker_cells.append(coord)
        elif type_ == Type.BONUS:
            self.stars.append(coord)

    def add_spear(self, arg):
        danger = Danger(arg[:2], Type.SPEAR, arg[2:])
        self._danger_objects.append(danger)

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

    def available_for_move(self, coord):
        bad_cells = self._blocker_cells + self._danger_cells
        for_check = map(partial(Dir.move, coord), Dir.ALL)
        check = lambda c: self._in_range(c) and c not in bad_cells
        return filter(check, for_check)

    def _in_range(self, coord):
        dy, dx = self.dim
        y, x = coord
        return 0 <= x < dx and 0 <= y < dy

    def init(self):
        is_empty = lambda c: not self._is_blocker(c)

        def init_danger(d):
            d.danger_cells[:] = []
            if d.type == Type.SPEAR:
                d.danger_cells.append(d.coord)
            elif d.type == Type.LASER:
                for _dir in d.dirs:
                    gen = Dir.move_generator(d.coord, _dir)
                    r = takewhile(is_empty, gen)
                    d.danger_cells.extend(list(r))
        map(init_danger, self._danger_objects)

    def set_time(self, time):
        if self._time == time: return
        self._time = time
        self._danger_cells[:] = []
        # print 'set_time', time
        for danger in self._danger_objects:
            self._danger_cells.extend(danger.pull(time))

    def is_valid(self):
        self.set_time(0)
        return self.start not in self._danger_cells

    def _is_blocker(self, coord):
        return coord in self._blocker_cells or not self._in_range(coord)

    @property
    def text(self):
        return self.take_text()

    txt = text

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
        dy, dx = self.dim
        level = dict()
        level['name'] = name
        level['size'] = [dx, dy]
        level['map'] = None
        level['symbols'] = None

        symbols = list()
        symbols.append({'symbol': '.', 'type': 'EMPTY'})
        symbols.append({'symbol': '#', 'type': 'WALL'})
        symbols.append({'symbol': 'o', 'type': 'START'})
        symbols.append({'symbol': '^', 'type': 'FINISH'})
        symbols.append({'symbol': '+', 'type': 'BONUS'})

        def set_symbol((y, x), symbol):
            art[y][x] = symbol

        get_symbol = lambda (y, x): art[y][x]

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