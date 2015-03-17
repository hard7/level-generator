from generator import Generator
from field import Type
from solver import *
from danger import Danger

from copy import deepcopy
from random import choice
from itertools import product, chain, count, izip
from operator import add, sub, itemgetter
from functools import partial
from utils import *
import collections
import BFS
from timer import Timer


class SpearGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def make_field(self, p=None):
        field = None
        while not field:
            field = self._make_field(p)
            if field and len(Solver(field).run()) > 5:
                field = None
        return field

    def _make_field(self, p=None):
        field = Field(self.dim)
        self.put_start_and_finish(field)
        self.put_bricks(field)
        # good_paths = self.get_good_paths(field)
        # if good_paths is None:
        #     print 'good_paths is None'
        #     return None
        # self.put_bonus(field, good_paths)
        paths = Solver(field).run()
        dv, descr = self.search_danger_variant(paths)
        return field

        # self._spear_filling(field, good_paths)

    def put_start_and_finish(self, field):
        start = self._choice_start_position()
        finish = get_reflection(self.dim, start)
        field.add_object(start, Type.START)
        field.add_object(finish, Type.FINISH)

    def put_bricks(self, field, _range=(26, 50)):
        ans = []
        field.save_backup()
        while len(ans) < _range[0] or len(ans) > _range[1]:
            wg = WallGen(self.dim, field.start, field.finish)
            wg.gen_loop()
            wg.gen_loop()
            wg.gen_bridge()

            field.load_backup()
            field.add_group(wg.get_bricks(), Type.BRICK)
            ans = Solver(field).run()

    @staticmethod
    def get_good_paths(field):
        ans = Solver(field).run()
        _size = len(ans) / 3
        ans = list(izip(*[iter(ans)]*_size))
        c0 = count(42, -1)
        while c0.next():
            paths = map(choice, ans)
            x, y, z = map(set, [a[3:-2] for a in paths])
            if all([(z & y & x), (z & y - x), (z - y - x)]):
                return paths
        return None

    @staticmethod
    def put_bonus(field, paths):
        x, y, z = map(set, [a[3:-2] for a in paths])
        bonus = (z & y & x), (z & y - x), (z - y - x)
        bonus = map(choice_from_set, bonus)
        field.add_group(bonus, Type.BONUS)

    @staticmethod
    def visit_time(cell, paths):
        res = []
        for i, path in enumerate(paths):
            if cell in path:
                time, path_i = path.index(cell), i
                res.append((time, path_i))
        return res

    @staticmethod
    def search_danger_variant(paths):
        at_stake = lambda (t, _): Danger.at_stake(per, t)
        slist = list()
        periods = Danger.make_all_period()
        free_cells = set(chain(p[1:-1] for p in paths))
        for cell in free_cells:
            times = SpearGenerator.visit_time(cell, paths)
            cur = list()
            for per in periods:
                bt = filter(at_stake, times)
                indexes = map(itemgetter(1), bt)
                if indexes:
                    cur.append(BFS.make_item(indexes, len(paths)))
            if cur:
                slist.append(cur)
        return slist, None

    @staticmethod
    def cell_to_danger_variant():
        pass

    def make_spear_list(self, field, good_paths):
        bad_paths = Solver(field).run()
        map(bad_paths.remove, good_paths)
        len_bad_paths = len(bad_paths)
        at_stake = lambda (t, _): Danger.at_stake(per, t)

        slist = list()
        periods = Danger.make_all_period()
        for cell in field.free_cells:
            good_times = self.visit_time(cell, good_paths)
            bad_times = self.visit_time(cell, bad_paths)
            cur = list()
            for per in periods:
                if filter(at_stake, good_times):
                    continue
                bt = filter(at_stake, bad_times)
                indexes = map(itemgetter(1), bt)
                if indexes:
                    # cur.add(frozenset(indexes))
                    cur.append(BFS.make_item(indexes, len_bad_paths))
            if cur:
                slist.append(cur)

        print field.take_text()
        with Timer():
            x = BFS.BFS(slist, len_bad_paths)
        # print 'x:', x
        return slist

    def _spear_filling(self, field, paths):
        field.save_backup()
        good_route = self.paths_to_map(paths)

        best_field_dict = None
        best_account = 100500

        c0 = count(10, -1)
        while best_account != 3 and c0.next():
            bad_paths = Solver(field).run()
            map(bad_paths.remove, paths)

            c1 = count(42, -1)
            while c1.next():
                bad_route = self.paths_to_map(bad_paths)
                coord, times = self.put_spear(field, good_route, bad_route)
                if coord is None:
                    break
                field.init()
                closed = [path for path in bad_paths
                          if coord in take_some(path, times)]
                map(bad_paths.remove, closed)

            sc = len(Solver(field).run())
            if sc < best_account:
                best_field_dict = deepcopy(field.__dict__)
                best_account = sc
            field.load_backup()
        field.__dict__ = best_field_dict

    @staticmethod
    def put_spear(field, good, bad):
        result = None
        source = field.free_cells[:]
        while not result and source:
            coord = choice_and_pop(source)
            good_per = good.get(coord, [])
            bad_per = bad.get(coord, [])

            if not bad_per:
                continue

            periods = Danger.make_all_period()
            while not result and periods:
                per = choice_and_pop(periods)
                g = map(Danger.at_stake_wrap(per), good_per).count(True)
                b = map(Danger.at_stake_wrap(per), bad_per).count(True)

                dan = partial(filter, Danger.at_stake_wrap(per), bad_per)
                result = dan() if (not g and b) else None

        if not result and not source:
            return None, None

        field.add_object(coord, Type.SPEAR, per)
        return coord, list(result)

    @staticmethod
    def paths_to_map(paths):
        _map = collections.defaultdict(set)
        src = chain(*map(enumerate, paths))
        [_map[val].add(i) for i, val in src]
        for key, val in _map.iteritems():
            _map[key] = sorted(val)
        return dict(_map)

    def _choice_start_position(self):
        wg = WallGen(self.dim, None, None)
        start = wg.fill(0, 0) - wg.fill(1, 1) - wg.corner(0, 0)
        return choice_from_set(start)

_sum = lambda r, l: tuple(map(add, r, l))
_bin_op = lambda opp, r, l: tuple(map(opp, r, l))


def make_rect(lo, sides):
    (x, y), (w, h) = lo, sides
    p = product(xrange(x, x+w+1), xrange(y, y+h+1))
    return set(p)


def make_rect_2(p1, p2):
    lo, hi = zip(*map(sorted, zip(p1, p2)))
    sides = _bin_op(sub, hi, lo)
    return make_rect(lo, sides)

class WallGen(object):
    CENTER = 1
    BORDER = 2
    CORNER = 4

    def __init__(self, dim, start, finish):
        self.dim = dim
        self.start = start
        self.finish = finish
        self.path_cells = set()
        self.brick_cells = set()
        self.eight_dirs = set(product(xrange(-1, 2), repeat=2))
        self.eight_dirs.discard((0, 0))
        self.four_dirs = set([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def gen_bridge(self):
        if not (self.extend_4(self.start) & self.path_cells):
            targets = self.fill(1, 1) & self.extend_8(self.start)
            targets -= self.path_cells
            if not targets:
                targets = self.fill(0, 0) & self.extend_4(self.start)
                self.path_cells.add(choice_from_set(targets))
            else:
                brick = choice_from_set(targets)
                self.brick_cells.add(brick)
                _path = self.extend_8(brick)
                _path.remove(self.start)
                self.path_cells |= _path

        if not (self.extend_4(self.finish) & self.path_cells):
            targets = self.fill(1, 1) & self.extend_8(self.finish)
            targets -= self.path_cells
            if not targets:
                targets = self.fill(0, 0) & self.extend_4(self.finish)
                self.path_cells.add(choice_from_set(targets))
            else:
                brick = choice_from_set(targets)
                self.brick_cells.add(brick)
                _path = self.extend_8(brick)
                _path.remove(self.finish)
                self.path_cells |= _path


    def fill(self, xo, yo):
        x, y = self.dim
        return set(product(xrange(xo, x-xo), xrange(yo, y-yo)))

    def corner(self, xo, yo):
        x, y = self.dim
        return set(product([xo, x-xo-1], [yo, y-yo-1]))

    def extend_9(self, coord):
        return set([coord] + map(partial(_sum, coord), self.eight_dirs))

    def extend_8(self, coord):
        return set(map(partial(_sum, coord), self.eight_dirs))

    def extend_4(self, coord):
        return set(map(partial(_sum, coord), self.four_dirs))

    def gen_loop(self, flag=7):
        source = set()
        if flag & WallGen.BORDER:
            source |= self.fill(1, 1) - self.fill(2, 2)
        if flag & WallGen.CORNER:
            source |= self.corner(1, 1)
        if flag & WallGen.CENTER:
            source |= self.fill(2, 2)
        self._gen_loop(source)

    def _gen_loop(self, source=None, count=1):
        source -= self.extend_9(self.start)
        source -= self.extend_9(self.finish)
        source -= self.path_cells
        source -= self.brick_cells

        assert source

        brick = choice_from_set(source)
        self.brick_cells.add(brick)
        self.path_cells |= self.extend_8(brick)

    def find_ponds(self):
        x, y = self.dim
        res = []
        for j in xrange(y-1):
            for i in xrange(x-1):
                p = set(product([i, i+1], [j, j+1]))
                if p <= self.path_cells:
                    res.append(p)
        return res

    def count_pond(self):
        return len(self.find_ponds())

    def get_bricks(self):
        x, y = self.dim
        res = set(product(xrange(x), xrange(y)))
        res -= set([self.start, self.finish])
        res -= self.path_cells
        return res