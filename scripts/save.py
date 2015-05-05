__author__ = 'anosov'
import os
import itertools


def save_fields2out(fields, out, base_name):
    c = itertools.count()
    for field in fields:
        name = base_name + '_' + str(c.next())
        name_exp = name + '.txt'
        path = os.path.join(out, name_exp)
        with open(path, 'w') as f:
            f.write(field.take_json(name))
