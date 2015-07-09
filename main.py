import solver
from field import Field
import pickle_cover
import pickle
from timer import Timer as T
import os
import scripts
import itertools
import matplotlib.pyplot as plt
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


def debug_making_covers():
    base = Field.load_by_json('base_field.json')
    print base.txt

if __name__ == '__main__':
    debug_making_covers()


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





