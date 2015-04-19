__author__ = 'hard7'
import os
import json


def set_level_name_by_filename(_inp):
    assert isinstance(_inp, str)
    filename_and_ext = os.path.split(_inp)[1]
    filename = os.path.splitext(filename_and_ext)[0]
    with open(_inp) as f:
        level = json.load(f)
        level['name'] = filename
    with open(_inp, 'w') as f:
        json.dump(level, f, indent=2, sort_keys=True)





if __name__ == '__main__':
    folder = '../trapped/Assets/Resources/Levels/m1'

    spl = lambda n: os.path.splitext(n)[1]
    names = filter(lambda name: spl(name) == '.txt', os.listdir(folder))
    for name in names:
        set_level_name_by_filename(os.path.join(folder, name))
