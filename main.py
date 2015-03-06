__author__ = 'anosov'

import types

from generator.easy_generator import EasyGenerator
from generator.generator_v2 import WallGen
from generator.generator_v2 import GeneratorV2, PathGen_temp, PathGenType, WallGen
from solver import Solver, Solver
from field import Field, Type, Dir
import operator, re
from functools import partial
from itertools import chain, count, compress, product, izip
from collections import defaultdict
from random import choice, randint, randrange
from utils import *
from copy import deepcopy
from generator.random_coord import UniqueRandomCoord


from path_finder import PathFinder


path_to_levels = 'result/levels/'
answer_path = 'result/answer.txt'

REQUIRED_FIELD_COUNT = 0


def _is_valid_field(field, result):
    assert isinstance(field, Field)
    if not result:
        return False
    else:
        len_result = len(result)-1
        return len_result and 10 <= len_result <= 16


def generate_valid_fields(gen, required_field_count, is_valid):
    assert isinstance(gen, EasyGenerator)
    assert isinstance(required_field_count, int)
    assert isinstance(is_valid, types.FunctionType)

    valid_fields = []
    field = result = None
    for _ in range(required_field_count):
        while True:
            field = generator.make_field()
            result = Solver(field).run()                # TODO func
            if result and is_valid(field, result[0]):
                break
        valid_fields.append((field, result[0]))
    return valid_fields

# --


def make_simple_field():
    field = Field(6, 6)
    field.add_object((1, 0), Type.HERO)
    field.add_object((4, 5), Type.FINISH)
    bricks = [(5, 0), (1, 1), (3, 1), (0, 3), (2, 3), (4, 3), (5, 3),
              (0, 4), (5, 4), (0, 5), (1, 5), (2, 5), (5, 5)]
    field.add_group(bricks, Type.BRICK)
    field.add_group([(4, 1), (1, 2), (3, 2)], Type.STAR)
    return field


move_map = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}


def one_step(start):
    one_step.coord = start

    def wrapper(char):
        one_step.coord = tuple(map(operator.add, one_step.coord, move_map[char]))
        return one_step.coord
    return wrapper


def make_path_for_simple_field(start=(1, 0)):
    return [start] + map(one_step(start), 'RUURUURU'), \
           [start] + map(one_step(start), 'RRRURULLUURU'), \
           [start] + map(one_step(start), 'RRRUULLLUURRRU')


def paths_to_routemap(paths):
    routemap = defaultdict(set)
    [routemap[val].add(i) for i, val in chain(*map(enumerate, paths))]
    for key, val in routemap.iteritems():
        routemap[key] = sorted(val)
    return dict(routemap)


def rand_period(_max=3):
    x0, x1 = randint(1, _max), randint(1, _max)
    return x0, x1, randrange(x0+x1)


def at_stake(step, on, off, offset):
    return (step + offset) % (on + off) < on


def at_stake_w(on, off, offset):
    return lambda step: at_stake(step, on, off, offset)


def choice_and_pop(array):
    item = choice(array)
    array.remove(item)
    return item


def make_all_period(_max=3):
    periods = product(range(1, _max+1), repeat=2)
    periods = [map(lambda offset: (on, off, offset),
                   range(on+off)) for on, off in periods]
    return list(chain(*periods))


def put_spear(field, good, bad):
    result = None
    source = field.free_cells[:]
    while not result and source:
        coord = choice_and_pop(source)
        good_per = good.get(coord, [])
        bad_per = bad.get(coord, [])

        if not bad_per:
            continue

        periods = make_all_period()
        while periods:
            per = choice_and_pop(periods)
            g = map(at_stake_w(*per), good_per).count(True)
            b = map(at_stake_w(*per), bad_per).count(True)
            if not g and b:
                result = compress(bad_per, map(at_stake_w(*per), bad_per))
                break

    if not result and not source:
        # print 'No have cells for put'
        return None, None

    field.add_object(coord, Type.SPEAR, per)

    return coord, list(result)


def item_at_any_position(array, element, positions):
    return element in take_some(array, positions)


def filling_using_spears(field, paths):
    field.save_backup()
    good_route = paths_to_routemap(paths)
    best_field = None
    best_account = 100500
    for _ in xrange(24):
        bad_paths = Solver(field).run()
        map(bad_paths.remove, paths)

        while True:
            bad_route = paths_to_routemap(bad_paths)
            coord, times = put_spear(field, good_route, bad_route)
            if coord is None:
                break
            field.init()
            closed = [path for path in bad_paths
                      if item_at_any_position(path, coord, times)]
            map(bad_paths.remove, closed)
        sc = len(Solver(field).run())
        if sc < best_account:
            best_field = deepcopy(field)
            best_account = sc
        field.load_backup()
    field.__dict__ = best_field.__dict__

import json


def make_field():
    dim = 6, 6
    wg = WallGen(dim, None, None)
    start = list(wg.fill(0, 0) - wg.fill(1, 1) - wg.corner(0, 0))
    start = choice(start)
    finish = get_reflection(dim, start)

    field = Field(*dim)
    field.add_object(start, Type.HERO)
    field.add_object(finish, Type.FINISH)
    field.save_backup()

    ans = []
    while not (26 < len(ans) < 50):
        w = WallGen(dim, start, finish)
        w.gen_loop()
        w.gen_loop()
        w.gen_bridge()

        field.load_backup()
        field.add_group(w.get_bricks(), Type.BRICK)
        ans = Solver(field).run()

    bonus = None
    c = count()
    while not bonus and c.next() < 40:
        _size = len(ans) / 3
        ans = izip(*[iter(ans)]*_size)
        ans = map(choice, ans)
        x, y, z = map(set, [a[3:-2] for a in ans])
        _bonus = (z & y & x), (z & y - x), (z - y - x)
        if all(map(len, _bonus)):
            bonus = map(choice, map(list, _bonus))

    if not bonus:
        return None

    field.add_group(bonus, Type.STAR)
    filling_using_spears(field, ans)
    return field


if __name__ == '__main__':
    c = count()
    for _ in xrange(50):
        f = None
        while not f:
            f = make_field()
        name = 'spear_%s' % c.next()
        print name
        text = f.take_json(name)

        file = open('gen_spear/' + name + '.txt', 'w')
        file.write(text)
        file.close()




def om():
    pass
    # generator = EasyGenerator(6, 6)
    # args = (generator, REQUIRED_FIELD_COUNT, _is_valid_field)
    # vf = generate_valid_fields(*args)
    #
    # field_names = {field: 'Gen #%i' % i for i, (field, _) in enumerate(vf)}
    # for (field, answer) in vf:
    #     name = field_names[field]
    #     field_str = field.to_string(name)

