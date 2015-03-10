from generator import Generator
from field import Type
from solver import *
from danger import Danger

from copy import deepcopy
from random import choice
from itertools import product, chain, count, izip, compress
from operator import add, sub
from functools import partial
from utils import *
import collections


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
        start = self._choice_start_position()
        finish = get_reflection(self.dim, start)

        field = Field(self.dim)
        field.add_object(start, Type.START)
        field.add_object(finish, Type.FINISH)
        field.save_backup()

        all_ans = []
        while len(all_ans) < 26 or len(all_ans) > 50:
            wg = WallGen(self.dim, start, finish)
            wg.gen_loop()
            wg.gen_loop()
            wg.gen_bridge()

            field.load_backup()
            field.add_group(wg.get_bricks(), Type.BRICK)
            all_ans = Solver(field).run()

        bonus = None
        c0 = count(42, -1)
        while not bonus and c0.next():
            _size = len(all_ans) / 3
            ans = map(choice, izip(*[iter(all_ans)]*_size))
            x, y, z = map(set, [a[3:-2] for a in ans])
            _bonus = (z & y & x), (z & y - x), (z - y - x)
            if all(map(len, _bonus)):
                bonus = map(choice_from_set, _bonus)

        if not bonus:
            return None

        field.add_group(bonus, Type.BONUS)
        self._spear_filling(field, ans)
        return field

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

    def make_field_deprecated(self, prop=None):
        self.random_coord.clear()
        c = self.x_coord, self.y_coord
        field = Field(*c)
        h = self.random_coord.get_on_border()
        f = self.random_coord.get_reflection(h)
        field.add_object(h, Type.START)
        field.add_object(f, Type.FINISH)

        field.save_backup()
        finish_paths, start_coords = None, None
        correct = lambda: bool(finish_paths and start_coords)
        c = int(self.cell_count/3.5)

        # while not correct():
        #     field.load_backup()
        #     # self._insert_few_brick(field, c)
        #     # self._insert_brick_with_loop(field, 3)
        #     self._insert_brick(field)
        #
        #     finish_paths, start_coords = 1, 1
        #         # find_correct_paths_and_starts(field)

        return field

    def _insert_few_brick(self, field, n=None):
        assert n is not None or n > 0
        brick_count = int(n if n else self.cell_count/3)
        brick_coords = self.random_coord.get_any_n(brick_count)
        field.add_group(brick_coords, Type.BRICK)

    def _insert_brick(self, field):
        x, y = field.dim
        free = set(product(xrange(x), xrange(y)))
        free.remove(field.get_start())
        free.remove(field.get_finish())

        self._insert_double_brick_with_loop(field, free, 3)
        self._insert_brick_with_loop(field, free, 5)

    def _insert_brick_with_loop(self, field, free, n):
        x, y = field.dim
        dirs = set(product(xrange(-1, 2), xrange(-1, 2)))
        add_ = lambda d: tuple(map(add, c, d))
        # free = set(product(xrange(x), xrange(y)))
        # free.remove(field.get_start())
        # free.remove(field.get_finish())
        for _ in xrange(n):
            if not free:
                return
            c = choice_from_set(free)
            busy = set(map(lambda d: add_(d), dirs))
            free -= busy
            field.add_object(c, Type.BRICK)

    def _insert_double_brick_with_loop(self, field, free, n):
        x, y = field.dim
        all_dirs = set(product(xrange(-1, 2), repeat=2))
        four_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        sum_ = lambda r, l: tuple(map(add, r, l))
        # free = set(product(xrange(x), xrange(y)))
        # free.remove(field.get_start())
        # free.remove(field.get_finish())
        for _ in xrange(n):
            if not free:
                print >> 'Free vector is empty'
                return
            c = choice_from_set(free)
            candidate = free & set(map(partial(sum_, c), four_dirs))
            if not candidate:
                raise Exception
            c2 = choice_from_set(candidate)

            busy = set(map(partial(sum_, c), all_dirs))
            busy |= set(map(partial(sum_, c2), all_dirs))

            free -= busy
            field.add_group([c, c2], Type.BRICK)



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


class PathGenType:
    ON_BORDER = 1
    IN_CORNER = 2
    ON_BORDER_OR_CORNER = 3


class EmptyObject(object): pass


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

class PathGen_temp(object):
    ATTEMPT_COUNT = 20

    def __init__(self, dim, start, finish):
        self.dim = dim
        self.start = start
        self.finish = finish
        x, y = dim
        self.free = set(product(xrange(x), xrange(y)))
        self.all_cells = self.free
        self.all_dirs = set(product(xrange(-1, 2), repeat=2))
        self.four_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.loops = []
        self.ponds = []

    def gen_loop(self, type_):
        _fl = lambda (x, y), xo=0, yo=0: set(product(xrange(xo, x-xo), xrange(yo, y-yo)))
        _br = lambda (x, y), xo=0, yo=0: set(product([xo, x-xo-1], [yo, y-yo-1]))
        _rou = lambda p, dirs: set(map(partial(_sum, p), dirs))

        fill = partial(_fl, self.dim)
        border = partial(_br, self.dim)
        round_all = partial(_rou, dirs=self.all_dirs)
        round_four = partial(_rou, dirs=self.four_dirs)

        if type_ == PathGenType.ON_BORDER:
            source = fill(1, 1) - fill(2, 2) - border(1, 1)
            used = round_all(self.start) | round_all(self.finish)
            source -= used
        elif type_ == PathGenType.IN_CORNER:
            used = round_all(self.start) | round_all(self.finish)
            source = border(1, 1) - used
        else:
            f = lambda r, l: r.union(set(l.shell | l.brick_set))
            reduce(f, self.loops, set())
            source = fill(1, 1) - reduce(lambda r, l: r.union(l.shell | l.brick_set), self.loops, set())
            source -= set([self.start, self.finish])
            source -= set(chain(*self.ponds))

        brick = choice_from_set(source)

        loop = EmptyObject()
        loop.brick = brick
        loop.brick_set = set([brick])
        loop.shell = round_all(brick) & self.all_cells - loop.brick_set

        # print loop.brick, loop.shell
        self.loops.append(loop)

        try:
            self.field.add_group(source, Type.BRICK)
        except AttributeError:
            print 'ERROR: self.field call trow AttributeError'

    gen_half_loop = None

    def gen_pond(self, loop):
        b = loop.brick
        x_dir = list(product([-1, 1], repeat=2))
        corn = map(partial(_sum, b), x_dir)
        res = map(lambda (c, d): make_rect_2(c, _sum(c, d)), product(corn, x_dir))
        block = [l.brick for l in self.loops] + [self.start, self.finish]
        valid = lambda arr, a, b_: set(arr) <= a and not (set(arr) & set(b_))
        res = filter(partial(valid, a=self.all_cells, b_=block), res)
        r = list(choice_from_set(res))
        self.ponds.append(r)

    def get_bricks(self):
        f = set(deepcopy(self.all_cells))
        f -= set([self.start, self.finish])
        f -= reduce(lambda res, l: res.union(l.shell), self.loops, set())
        f -= set(chain(*self.ponds))
        # print self.ponds
        return f

    gen_half_pond = None

# g2 = GeneratorV2(7, 5)
# f = g2.make_field()
# print f.to_string('Easy')
#
# ps = PathStorage(f)

# import itertools
# print list(itertools.combinations([1, 4], 3))