__author__ = 'anosov'

import cell as cell_module
from cell import CellType
import collections
import itertools
import inspect
import utils


class x_Field:
    def __init__(self, *args):
        self._dim = args if len(args) == 2 else args[0]
        self._field = self.get_inited()
        self._blocker = list()
        self._location = collections.defaultdict(list)

    @property
    def dim(self):
        return self._dim

    def add(self, *args):
        param = list()
        is_cell = lambda a: isinstance(a, cell_module.Cell)
        is_factory = lambda a: inspect.isclass(a) and issubclass(a, cell_module.Cell)

        for arg in args:
            if is_cell(arg):
                self._add_one(arg)
            elif is_factory(arg):
                if not param:
                    self._add_one(param[0](*param[:1]))
                    param[:] = list()
                factory = arg
            else:
                param.append(arg)

        if factory is not None:
            self._add_one(factory(*param))

        raise NotImplementedError



    # def add(self, *args):
    #     for_construct = collections.defaultdict(list)
    #     is_sub = lambda a: inspect.isclass(a) and issubclass(a, cell_module.Cell)
    #     current = None
    #     for arg in args:
    #         if isinstance(arg, cell_module.Cell):
    #             self._add_one(arg)
    #         elif is_sub(arg): current = arg
    #         else: for_construct[current].append(arg)
    #     [self._add_one(func(*args)) for func, args in for_construct.iteritems()]

    def get_inited(self):
        coordinates = itertools.product(*map(xrange, self._dim))
        return {c: cell_module.Floor(c) for c in coordinates}

    def _add_one(self, cell):
        f = self._field
        cur = f.get(cell.coord, None)
        assert isinstance(cur, cell_module.Floor)
        cell.transplant_danger_source(f[cell.coord])
        f[cell.coord] = cell
        if cell.is_blocked():
            self._blocker.append(cell.coord)
            for laser_coord in self._location[CellType.LASER]:
                for shadow_coord in self[laser_coord].shading(cell.coord):
                    self[shadow_coord].del_danger_source(laser_coord)

        self._location[cell.type].append(cell.coord)
        if cell.type == CellType.SPEAR:
            cell.add_danger_source(cell.coord, cell.period)
        elif cell.type == CellType.LASER:
            cell.init_rays(self._blocker, self.dim)
            for danger in cell.danger:
                self[danger].add_danger_source(cell.coord, cell.period)

    def get_valid_moves(self, path, keys, step):
        raise NotImplementedError

    def __getitem__(self, item):
        return self._field[item]

    def __setitem__(self, key, value):
        self._field[key] = value



x = x_Field(6, 8)

x.add(cell_module.Laser, (1, 1), (1, 1, 1), (0, 1, 0, 0), cell_module.Laser, (1, 4), (1, 1, 1), (0, 0, 0, 1))

print x[1, 1].danger_source