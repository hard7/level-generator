__author__ = 'anosov'

from itertools import product
import collections
import field


def init_template_field_by_ascii(_map):
    row_lens = set(len(row) for row in _map)
    assert len(row_lens) == 1
    dy = len(_map)
    dx = row_lens.pop()
    inverse = lambda y, x: (dy-y-1, x)
    symbol2coord = collections.defaultdict(set)
    for (y, x) in product(xrange(dy), xrange(dx)):
        symbol2coord[_map[y][x]].add(inverse(y, x))
    start_symbols = 'o', 's', 'S'
    finish_symbols = '^', 'f', 'F'
    wall_symbols = '#', 'x', 'X'
    union_sets = lambda gen_set: list(set.union(*gen_set))
    start = union_sets(symbol2coord.get(s, set()) for s in start_symbols)
    finish = union_sets(symbol2coord.get(s, set()) for s in finish_symbols)
    walls = union_sets(symbol2coord.get(s, set()) for s in wall_symbols)
    assert len(start) == 1 and len(finish) == 1

    tmpl = field.Field((dy, dx))
    tmpl.add_object(start[0], field.Type.START)
    tmpl.add_object(finish[0], field.Type.FINISH)
    tmpl.add_group(walls, field.Type.WALL)
    return tmpl




    # def make_f(start, finish, walls):
    #     f = Field(map(len, [_map, _map[0]]))
    #     f.add_object(start, Type.START); f.add_object(finish, Type.FINISH)
    #     f.add_group(walls, Type.WALL)
    #     return f
    # take_obj = lambda var: lambda (j, row): [var[item].append((j, i)) for i, item in enumerate(row)]
    # values = lambda var=defaultdict(list): [map(take_obj(var), enumerate(_map)), var][1]
    # args = lambda (x, y, z)=map(values().get, 'o^x'): [x[0], y[0], z]
    # return make_f(*args())