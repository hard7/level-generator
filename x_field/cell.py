__author__ = 'anosov'

import itertools
from coord import Coord

class CellType:
    COUNT_TYPES = 11
    START, FINISH, FLOOR, PIT, WALL, KEY, DOOR, \
        BONUS, PORTAL, SPEAR, LASER = range(COUNT_TYPES)


class Cell(object):
    def __init__(self, coord, ctype, blocked=False):
        self._coord = coord
        self._blocked = blocked
        self._danger_sources = dict()
        self._ctype = ctype

    def add_danger_source(self, cell, period):
        self._danger_sources[cell] = period

    def del_danger_source(self, cell):
        del self._danger_sources[cell]

    def transplant_danger_source(self, other):
        assert isinstance(other, Cell)
        self._danger_sources = other._danger_sources.copy()

    @property
    def coord(self):
        return self._coord

    @property
    def type(self):
        return self._ctype

    @property
    def danger_source(self):
        return self._danger_sources.keys()

    def is_blocked(self):
        return self._blocked

    def __hash__(self):
        return hash(self.coord)

class Pit(Cell):
    def __init__(self, coord):
        super(self.__class__, self).__init__(coord, CellType.PIT)


class Floor(Cell):
    def __init__(self, coord):
        super(self.__class__, self).__init__(coord, CellType.FLOOR)


class Wall(Cell):
    def __init__(self, coord):
        super(self.__class__, self).__init__(coord, CellType.WALL, blocked=True)


class Start(Cell):
    def __init__(self, coord):
        super(self.__class__, self).__init__(coord, CellType.START)


class Bonus(Cell):
    def __init__(self, coord, hang=False):
        super(self.__class__, self).__init__(coord, CellType.BONUS)


class Finish(Cell):
    def __init__(self, coord, hang=False):
        super(self.__class__, self).__init__(coord, CellType.FINISH)
        self.hang = hang


class Tag:
    def __init__(self, tag):
        self.tag = tag


class Period:
    def __init__(self, *args):
        if len(args) == 1:
            self.period = args[0]
        elif len(args == 3):
            self.period = args
        else:
            raise Exception


def inside(coord, *args):
    c = Coord(coord)
    if len(args) == 1:
        args = (0,) + args
    _min, _max = map(Coord, args)
    return _min.y <= c.y < _max.y and _min.x <= c.x < _max.x


class Direct:
    # ALL = Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(-1, -1)
    ALL = (1, 0), (0, 1), (-1, 0), (0, -1)
    UP, RIGHT, DOWN, LEFT = ALL

    @staticmethod
    def make_ray(dim, base, _dir):
        dim = Coord(dim)
        coord = Coord(base)
        _dir = Coord(_dir)
        result = []
        while inside(coord.reset(coord + _dir), dim):
            result.append(coord.dat)
        return result

class Key(Cell):
    def __init__(self, coord, tag, hang=False):
        super(self.__class__, self).__init__(coord, CellType.KEY)
        self.tag = tag if isinstance(tag, Tag) else Period(tag)
        self.hang = hang


class Door(Cell):
    def __init__(self, coord, tag):
        super(self.__class__, self).__init__(coord, CellType.DOOR, blocked=True)
        self.tag = tag if isinstance(tag, Tag) else Period(tag)


class Portal(Cell):
    def __init__(self, coord, tag, hang=False):
        super(self.__class__, self).__init__(coord, CellType.PORTAL)
        self.tag = tag if isinstance(tag, Tag) else Period(tag)
        self.hang = hang


class Spear(Cell):
    def __init__(self, coord, period):
        if isinstance(period, int):
            period = map(int, str(period))
        super(self.__class__, self).__init__(coord, CellType.SPEAR)
        self._period = period if isinstance(period, Period) else Period(period)

    @property
    def period(self):
        return self._period


class Laser(Cell):
    def __init__(self, coord, period, directs):
        if isinstance(period, int):
            period = map(int, str(period))

        if isinstance(directs, str):
            directs = map(int, directs)

        super(self.__class__, self).__init__(coord, CellType.LASER, blocked=True)
        self._period = period if isinstance(period, Period) else Period(period)
        directs = itertools.compress(Direct.ALL, directs)
        self._ray = {i: None for i in directs}
        self._len = {i: 0 for i in directs}

    def init_rays(self, blocker, dim):
        for direct in self.directs:
            self._ray[direct] = Direct.make_ray(
                dim, self.coord, direct)
            self._len[direct] = len(self._ray[direct])
        map(self.shading, blocker)

    def shading(self, coord):
        result = list()
        for _dir in self.directs:
            ray = self._ray[_dir]
            if coord in ray:
                # new_len = ray.index(coord)
                new_len = ray.index(coord) + 1
                cur_len = self._len[_dir]
                if new_len < cur_len:
                    result.extend(ray[new_len-1:cur_len])
                    self._len[_dir] = new_len
        return result


    @property
    def danger(self):
        r, l = self._ray, self._len
        reduce_func = lambda res, k: res + r[k][:l[k]]
        return reduce(reduce_func, self.directs, list())

    @property
    def period(self):
        return self._period

    @property
    def directs(self):
        return self._ray.keys()