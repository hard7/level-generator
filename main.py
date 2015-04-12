from generator.spear_generator import SpearGenerator
from field import Field
from solver import solve, path_to_str, Solver
import cPickle
from pickle_cover import save_template_covers, to_cover
import itertools
from itertools import takewhile, chain, count, repeat
import operator
import utils
from collections import defaultdict
from functools import partial
from timer import Timer
from danger import Type     # TODO REPLACE
import os
import copy

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


def save_covers(inp_folder, out_folder, _count):
    names = filter(lambda s: s.endswith('.txt'), os.listdir(inp_folder))
    names.sort()
    for name in names:
        inp = os.path.join(inp_folder, name)
        out = os.path.join(out_folder, os.path.splitext(name)[0])
        assert not os.path.exists(out)
        os.mkdir(out)
        with Timer(name):
            save_template_covers(inp, out, _count)

def make_levels():
    index = 6
    path_to_dir = '../#output/covers/t' + str(index)
    with open(path_to_dir + '/template.json') as f:
        field = Field.load_by_file(f)
    field.save_backup()

    c0 = utils.Count()
    c1 = utils.Count()
    best = 0
    with open(path_to_dir + '/covers_1.dump') as f:
        known_paths = []
        while True:
            try:
                paths, spears = cPickle.load(f)
                field.load_backup()
                map(field.add_spear, spears)

                # print field.txt
                solver = Solver(field)
                solver.run()
                # print 'path', solver.win_paths[0]
                # print 'all move count', solver.move_count
                if solver.move_count > best:
                    best = solver.move_count


                print 'cur/best/count: %i / %i / %i' % (solver.move_count, best, c0.next())
                if solver.move_count > 100 and solver.win_paths[0] not in known_paths:
                    print '---------------------------------------------------'
                    known_paths.append(solver.win_paths[0])
                    path_to_out_file = '../#output/h_lev/lev_%i_%i.txt' % (index, c1.next())
                    assert not os.path.exists(path_to_out_file)
                    with open(path_to_out_file, 'w') as fx:
                        fx.write(field.take_json())
                    if c1.current == 2:
                        break
                        # print 'path', solver.win_paths[0]
                        # if raw_input('Next?') != '':
                        #     break
            except EOFError:
                break

def load_by_ascii(_map, name=None): # add assert
    def make_f(start, finish, walls):
        f = Field(map(len, [_map, _map[0]]))
        f.add_object(start, Type.START); f.add_object(finish, Type.FINISH)
        f.add_group(walls, Type.WALL)
        return f
    take_obj = lambda var: lambda (j, row): [var[item].append((j, i)) for i, item in enumerate(row)]
    values = lambda var=defaultdict(list): [map(take_obj(var), enumerate(_map)), var][1]
    args = lambda (x, y, z)=map(values().get, 'o^x'): [x[0], y[0], z]

    # print map(values().get, 'o^x')

    return make_f(*args())


def load_group_by_ascii(f):
    if isinstance(f, str):
        with open(f) as _f: return load_group_by_ascii(_f)

    lines = lambda: itertools.imap(utils.xrun('strip'), f.readlines())
    chunk_and_blank = lambda: map(partial(takewhile, bool), itertools.repeat(lines(), 128))
    chank = lambda: filter(bool, map(list, chunk_and_blank()))
    return [load_by_ascii(ch[:0:-1], ch[0]) for ch in chank()]


def move_count(field):
    field.save_backup()
    def wrapper((_, spears)):
        map(field.add_spear, spears)
        s = Solver(field); s.run()
        field.load_backup()
        return s.move_count
    return wrapper

if __name__ == '__main__':
    _input, _output = '../#input/tmpl_test.txt', '/#output/h2'

    cover = lambda n=1000, f=load_group_by_ascii(_input): \
        zip(f, map(partial(to_cover, count=n), f))

    def sorting((field, covers)):
        covers.sort(key=move_count(field), reverse=True)

    # print map(len, map(solve, load_group_by_ascii(_input)))
    # print map(move_count(fields[0]), c[0][1])
    # map(sorting, cover())

    def choice_cover(field, covers, n=2):
        field.save_backup()
        count_moves = defaultdict(list)
        for i, cover in enumerate(covers):
            map(field.add_spear, cover[1])
            s = Solver(field)
            s.run()
            count_moves[s.move_count].append(i)
            field.load_backup()
        sort_mv_count = lambda: sorted(count_moves.keys(), reverse=True)
        all_indexes = lambda: chain(*map(count_moves.get, sort_mv_count()))
        final_indexes = lambda c=count(): takewhile(lambda _: c.next() < n, all_indexes())
        return field, map(utils.xget(obj=covers), final_indexes())

    print list(itertools.starmap(partial(choice_cover, n=2), cover(3)))


