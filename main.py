__author__ = 'anosov'

import types

from generator.easy_generator import EasyGenerator
from generator.generator_v2 import GeneratorV2, PathGen, PathGenType
from solver import Solver, Solver
from field import Field
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


if __name__ == '__main__':
    g = GeneratorV2(6, 6)
    f = g.make_field()

    pg = PathGen(f.dim, f.get_start(), f.get_finish())
    # pg.field = f

    pg.gen_loop(PathGenType.ON_BORDER)
    pg.gen_pond(pg.loops[0])
    pg.gen_loop(66)
    # pg.gen_loop(PathGenType.IN_CORNER)

    # del pg.field

    from generator import Type
    f.add_group(pg.get_bricks(), Type.BRICK)

    print f.to_string()


    # g = GeneratorV2(6, 6)
    # f = g.make_field()
    # print f.to_string()
    # pf = PathFinder(f)

    # print [i for i in pf.gen_next(0, 2, 6)]
    # t = pf.make_triples(2, 5)
    # for i in t:
    #     print i

    # print 'path count:', len(pf.paths)
    # print 'triple count:', len(t)

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

