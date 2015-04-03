from generator import Generator
from field import Type
from solver import *
from danger import Danger, Dir
from copy import deepcopy
from random import choice
from itertools import product, chain, count, izip
from operator import add, sub, itemgetter
import operator as op
from functools import partial
from utils import *
import collections
import bfs
from timer import Timer
from wall_gen import WallGen
from random import shuffle
from danger_field.danger_field import DField
import pickle
import pprint


class SpearGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def make_field(self, p=None):
        return self._make_field(p)
        # while True:
        #     f = self._make_field(p)
        #     print f, len(Solver(f).run())
        #     if f and len(Solver(f).run()) > 5:
        #         return f

    def _make_field(self, p=None):
        field = self.get_template('prepared')
        with nested_break_contextmanager() as nested_break:
            for covers in DField(field, 1):
                for free_paths, spears in covers:

                    if len(spears) < 5:
                        break

                    # used_cells = len(set(chain(*free_paths)))
                    # if used_cells < 17:
                    #     break

                    map(field.add_spear, spears)
                    raise nested_break

                    # scoords = set(map(xgetitem[0:2], spears))
                    # bonus_variants = self.get_bonus_variants(free_paths)
                    # [op.isub(b, scoords) for b in bonus_variants]
                    # if all(bonus_variants):
                    #     bonus = map(choice_from_set, bonus_variants)
                    #     field.add_group(bonus, Type.BONUS)
                    #     map(field.add_spear, spears)
                    #
                    #     # for i in free_paths: print path_to_str(i)
                    #
                    #     if self.check_bonus_is_failed(field):
                    #         x, y, z = map(set, [a[3:-2] for a in sorted(free_paths, key=len)])
                    #         # print sorted(free_paths, key=len)
                    #         print z
                    #         print y
                    #         print x
                    #         print
                    #         print z & y & x
                    #         print z & y - x
                    #         print z - y - x
                    #     raise nested_break

        return field

    def get_template(self, key='generate'):
        if key.lower() == 'generate':
            return self._generate_template()
        elif key.lower() == 'prepared':
            return self._get_prepared_template()
        else:
            raise RuntimeError('Wrong key %s' % str(key))

    def _generate_template(self):
        field = Field(self.dim)
        self.put_start_and_finish(field)
        self.put_bricks(field)
        return field

    def _get_prepared_template(self):
        with open('../#input/t2.txt') as f:
            field = Field.load_by_file(f)
        self.dim = field.dim
        return field

    @staticmethod
    def check_bonus_is_failed(field):
        _list = [0, 0, 0]
        c = itertools.count()
        for path in sorted(solve(field), key=len):
            col = itertools.product(path, field.stars)
            _list[c.next()] = sum(itertools.starmap(operator.contains, col))
        return _list.sort() != [1, 2, 3]

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
            field.add_group(wg.get_bricks(), Type.WALL)
            ans = Solver(field).run()

    @staticmethod
    def get_bonus_variants(paths):
        x, y, z = map(set, [a[3:-2] for a in sorted(paths, key=len)])
        return z & y & x, z & y - x, z - y - x

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