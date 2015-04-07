from generator.spear_generator import SpearGenerator
from field import Field
from solver import solve, path_to_str
import cPickle
from pickle_cover import save_template_covers
import itertools
import operator
import utils
from collections import defaultdict
from timer import Timer
import os

def make(pack, n=1, ext=False):
    def make_one(i):
        field = gen.make_field()
        name = '%s_%i' % (pack, i)
        path = '/ExternalLevels/%s.txt' % name if ext else \
            '../#output/%s/%s.txt' % (pack, name)
        with open(path, 'w') as f:
            f.write(field.take_json(name))

    gen = SpearGenerator((6, 6))
    map(make_one, xrange(n))


def compare():
    with open('dumps/gen_field.dump') as f:
        from_pickle = pickle.load(f)

    with open('/ExternalLevels/level.txt') as f:
        from_json = Field.load_by_file(f)

    assert isinstance(from_pickle, Field)
    assert isinstance(from_json, Field)

    from_pickle_solves = sorted(map(tuple, solve(from_pickle)))
    from_json_solve = sorted(map(tuple, solve(from_json)))
    assert from_pickle_solves == from_json_solve


def provocation():
    gen = SpearGenerator((6, 6))
    gen_field = gen._make_field()
    json_path = '/ExternalLevels/level.txt'
    with open(json_path, 'w') as f:
        f.write(gen_field.take_json('level'))

    with open('dumps/gen_field.dump', 'w') as f:
        pickle.dump(gen_field, f)

    with open(json_path) as f:
        field_from_json = Field.load_by_file(f)

    gen_field_solves = sorted(map(tuple, solve(gen_field)))
    field_from_json_solves = sorted(map(tuple, solve(field_from_json)))
    assert gen_field_solves == field_from_json_solves


def test():
    gen = SpearGenerator(6, 7)
    gen_field = gen.make_field()
    json_path = '/ExternalLevels/level.txt'
    with open(json_path, 'w') as f:
        f.write(gen_field.take_json('level'))

if __name__ == '__main__':
    inp_folder = '../#input/templates'
    out_folder = '../#output/covers'

    names = filter(lambda s: s.endswith('.txt'), os.listdir(inp_folder))
    names.sort()
    for name in names:
        inp = os.path.join(inp_folder, name)
        out = os.path.join(out_folder, os.path.splitext(name)[0])
        os.mkdir(out)
        with Timer(name):
            save_template_covers(inp, out, 50000)