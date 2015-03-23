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
import bfs
from timer import Timer
from wall_gen import WallGen
from random import shuffle
from danger_field.danger_field import DField
import pickle


class SpearGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def make_field(self, p=None):
        while True:
            f = self._make_field(p)
            if f and len(Solver(f).run()) > 5:
                return f

    def _make_field(self, p=None):
        # field = Field(self.dim)
        # self.put_start_and_finish(field)
        # self.put_bricks(field)
        #
        # print field.take_text()

        with open('fish.dat') as f:
            field = pickle.load(f)

        print '>', len(Solver(field).run())

        field.add_object((0, 3), Type.SPEAR, (1, 1, 0))
        print field.take_text()

        print '>', len(Solver(field).run())


        # c = count()
        # for covers in DField(field):
        #     if covers:
        #         break
        #
        # field.save_backup()
        #
        # for cover in covers:
        #     paths, spears = cover
        #     field.load_backup()
        #     for spear in spears:
        #         field.add_object(spear[:2], Type.SPEAR, spear[2:])
        #
        #     res = Solver(field).run()
        #     print field.take_text()
        #     print len(spears), len(res)

        return field

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
    def gen_danger_type(paths):
        at_stake = lambda (t, _): Danger.at_stake(per, t)
        periods = Danger.make_all_period()
        free_cells = chain(p[1:-1] for p in paths)
        free_cells = list(set(free_cells))
        shuffle(free_cells)
        out_cells = []
        for cell in free_cells:
            out_cells.append(cell)
            times = SpearGenerator.visit_time(cell, paths)
            cur = []
            for per in periods:
                times = filter(at_stake, times)
                indexes = map(itemgetter(1), times)
                if indexes:
                    cur.append(bfs.make_item(indexes, len(paths)))
                    # cur_d.append(per)
            yield cur


    @staticmethod
    def search_danger_variant(paths):
        at_stake = lambda (t, _): Danger.at_stake(per, t)
        slist = list()
        descr = list()
        periods = Danger.make_all_period()
        free_cells = set(chain(p[1:-1] for p in paths))
        for cell in free_cells:
            times = SpearGenerator.visit_time(cell, paths)
            cur, cur_d = list(), list()
            for per in periods:
                _times = filter(at_stake, times)
                indexes = map(itemgetter(1), _times)
                if indexes:
                    cur.append(bfs.make_item(indexes, len(paths)))
                    cur_d.append(per)
            if cur:
                slist.append(cur)
                descr.append(cur_d)
        return slist, None

    def _choice_start_position(self):
        wg = WallGen(self.dim, None, None)
        start = wg.fill(0, 0) - wg.fill(1, 1) - wg.corner(0, 0)
        return choice_from_set(start)