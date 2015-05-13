import scripts
import solver
from field import Field
import pickle_cover
import pickle
from timer import Timer as T
import os

conf = dict()
conf['path'] = '../data/f0'
conf['field'] = os.path.join(conf['path'], 'field.json')
conf['covers'] = os.path.join(conf['path'], 'covers.dump')


if __name__ == '__main__':
    # gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    # fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    # field = fields[0]

    # with T():
    #     covers_ret = pickle_cover.to_cover(field, max_spear=18, max_answer=5000)
    #     covers = [cov[1] for cov in covers_ret]

    with T():
        field = Field.load_by_json(conf['field'])
        covers = pickle_cover.load(conf['covers'])

    map(field.add_spear, covers[0])


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





