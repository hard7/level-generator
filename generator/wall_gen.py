from itertools import *
from operator import add, sub
from utils import *
from functools import partial

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