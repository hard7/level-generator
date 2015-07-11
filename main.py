import solver
from field import Field
import pickle_cover
import cPickle
from timer import Timer as T
import os
import scripts
import itertools
# import matplotlib.pyplot as plt
from cover_sort.data_processing import DataProcessing
from functools import partial


def add_parameter(dict_, parameter, ext='dump'):
    root_path = dict_.setdefult('path', '/home/anosov/data/f0')
    dict_[parameter] = os.path.join(root_path, '%s.%s' % (parameter, ext))

# conf = dict()
# add_parameter(conf, 'field', 'json')
# add_parameter(conf, 'covers')
# add_parameter(conf, 'apl')
# add_parameter(conf, 'ans_len')
# add_parameter(conf, 'walked_spear')
# add_parameter(conf, 'field_min_max')


# conf['field'] = os.path.join(conf['path'], 'field.json')
# conf['covers'] = os.path.join(conf['path'], 'covers.dump')
# conf['apl'] = os.path.join(conf['path'], 'apl.dump')
# conf['ans_len'] = os.path.join(conf['path'], 'ans_len.dump')
# conf['walked_spear'] = os.path.join(conf['path'], 'walked_spear.dump')
# conf['field_min_max'] =  os.path.join(conf['path'], 'field_min_max.dump')


def dump_current_field_covers():
    def unique_append(list_, item):
        if item not in list_:
            list_.append(item)
        return list_.index(item)

    pr_periods = list()
    pr_cells = list()
    pr_paths = list()
    pr_covers = list()
    pr_cover_paths = list()

    base = Field.load_by_json('base_field.json')

    with T():
        path_and_spears_group = pickle_cover.to_cover(base, max_spear=18, max_answer=1000)

    for path, spears in path_and_spears_group:
        new_cover = list()
        for spear in spears:
            cell, period = spear[:2], spear[2:]
            cell_id = unique_append(pr_cells, cell)
            period_id = unique_append(pr_periods, period)
            new_cover.append((cell_id, period_id))
        pr_covers.append(tuple(new_cover))

        new_path = list()
        for cell in path[0]:
            cell_id = unique_append(pr_cells, cell)
            new_path.append(cell_id)
        path_id = unique_append(pr_paths, tuple(new_path))
        pr_cover_paths.append(path_id)

    dump_dict = dict()
    dump_dict['base'] = base.take_json()
    dump_dict['periods'] = pr_periods
    dump_dict['cells'] = pr_cells
    dump_dict['paths'] = pr_paths
    dump_dict['covers'] = pr_covers
    dump_dict['cover_paths'] = pr_cover_paths

    with open('../test_1k_covers.dump', 'w') as f:
        cPickle.dump(dump_dict, f)

if __name__ == '__main__':
    dump_current_field_covers()


def analyze():
    # gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    # fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    # field = fields[0]

    # with T():
    #     covers_ret = pickle_cover.to_cover(field, max_spear=18, max_answer=20000)
    #     covers = [cov[1] for cov in covers_ret]
    #
    # with T():
    #     with open(conf['field'], 'w') as f:
    #         f.write(field.take_json())
    #     pickle_cover.dump(covers, conf['covers'])

    # with T('alternative_path_lens'):
    #     apl = map(scripts.alternative_path_lens, scripts.covered(t_field, covers))
    #     pickle_cover.dump(apl, conf['apl'])

    # with T('ans_len'):
    #     ans_len = map(len, itertools.imap(solver.solve_one, scripts.covered(t_field, covers)))
    #     pickle_cover.dump(ans_len, conf['ans_len'])

    # with T('walked_spear'):
    #     sc = scripts
    #     isec = lambda f: set(solver.solve_one(c)) & set(c.get_spear_coords())
    #     walked_spear = [len(isec(c)) for c in sc.covered(t_field, covers)]
    #     pickle_cover.dump(walked_spear, conf['walked_spear'])

    # with T('field_min_max'):
    #     lens = map(len, solver.solve(t_field))
    #     field_min_max = min(lens), max(lens)
    #     pickle_cover.dump(field_min_max, conf['field_min_max'])

    with T('Load'):
        t_field = Field.load_by_json(conf['field'])
        covers = pickle_cover.load(conf['covers'])
        apl = pickle_cover.load(conf['apl'])
        ans_len = pickle_cover.load(conf['ans_len'])
        walked_spear = pickle_cover.load(conf['walked_spear'])
        field_min_max = pickle_cover.load(conf['field_min_max'])

    with T('work'):
        dp = DataProcessing(t_field, covers)
        dp.solver
        dp.alternative_path_len

    """
    Mark(len_path, spear_walked, alt_path_depth, alt_path_width)
    """




    # map(field.add_spear, covers[0])


        # dump = '../x.dmp'
        # import pickle
        # with open(dump, 'r') as _file:
        #     f = pickle.load(_file)


def act():
    gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    fields = fields[:1]

    scripts.show_path_count_for_fields(fields)
    g = scripts.calc_covered_gen(fields[0])

    while not raw_input('>'):
        scripts.save_fields2out([g.next()], '/ExternalLevels', 'lev')





