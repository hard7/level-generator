from generator.spear_generator import SpearGenerator
from field import Field
from solver import solve, path_to_str
import pickle
import itertools
import operator
import utils


def make():
    def make_one(i):
        field = gen.make_field()
        name = 'spear_%i' % i
        out = open('gen_spear/%s.txt' % name, 'w')
        out.write(field.take_json(name))
        out.close()

    gen = SpearGenerator((6, 6))
    map(make_one, xrange(50))


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

    # print gen_field_solves
    # print field_from_json_solves


if __name__ == '__main__':
    provocation()