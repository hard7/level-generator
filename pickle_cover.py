__author__ = 'anosov'

from field import Field
from danger_field.danger_field import DField
import os
import shutil
import cPickle
from functools import partial
import utils


def save_template_covers(_field, output_folder, answer_count):
    if isinstance(_field, str) or isinstance(_field, file):
        field = lambda: Field.load_by_json(_field)
        return save_template_covers(field(), output_folder, answer_count)

    is_empty_dir = lambda s: not os.listdir(s)
    assert isinstance(_field, Field)
    assert os.path.isdir(output_folder)
    assert is_empty_dir(output_folder)

    ids = [1, 2, 3]
    out_path = partial(os.path.join, output_folder)
    DF = partial(DField, _field, requared_path_count=ids)
    DF = partial(DF, max_spear=10, max_answer=answer_count)
    mk_f = lambda x: open(out_path('covers_%i.dump' % x), 'wb', buffering=0)
    dump = lambda fls: lambda c: cPickle.dump(c, fls[len(c[0])]-1)
    close = lambda fls: partial(map, utils.xrun('close'))
    complete = lambda files=map(mk_f, ids): [map(dump(files), DF()), close(files)]

    complete()
    with open(out_path('template.json'), 'w') as f:
        f.write(_field.take_json())


def to_cover(field, count=None):
    return list(DField(field, max_spear=14, max_answer=count))


def save_covers(inp_folder, out_folder, _count):
    names = filter(lambda s: s.endswith('.txt'), os.listdir(inp_folder))
    names.sort()
    for name in names:
        inp = os.path.join(inp_folder, name)
        out = os.path.join(out_folder, os.path.splitext(name)[0])
        assert not os.path.exists(out)
        os.mkdir(out)
        save_template_covers(inp, out, _count)