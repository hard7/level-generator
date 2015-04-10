__author__ = 'anosov'

from field import Field
from danger_field.danger_field import DField
import os
import shutil
import cPickle
from functools import partial


def save_template_covers(input_file, output_folder, answer_count):
    is_empty_dir = lambda s: not os.listdir(s)
    assert os.path.isfile(input_file)
    assert os.path.isdir(output_folder)
    assert is_empty_dir(output_folder)

    out_path = partial(os.path.join, output_folder)
    shutil.copy2(input_file, out_path('template.json'))

    with open(out_path('template.json'), 'r') as f:
        field = Field.load_by_file(f)

    path_count = [1, 2, 3]
    d_field = DField(field, requared_path_count=path_count, max_spear=10, max_answer=answer_count)

    # with open(out_path('paths.dump'), 'wb') as f:
    #     cPickle.dump(d_field.paths, f)

    f1 = open(out_path('covers_1.dump'), 'wb', buffering=0)
    f2 = open(out_path('covers_2.dump'), 'wb', buffering=0)
    f3 = open(out_path('covers_3.dump'), 'wb', buffering=0)
    f = lambda idx: [f1, f2, f3][idx]
    with f1, f2, f3:
        for covers in d_field:
            for cover in covers:
                index = len(cover[0])-1
                cPickle.dump(cover, f(index))


def to_cover(field, count=None):
    return list(DField(field, max_spear=14, max_answer=count))