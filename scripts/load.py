__author__ = 'anosov'
import re
import itertools
import field


def take_template_ascii_from_file(path):
    with open(path) as f:
        raw_txt = f.read()

    splited = raw_txt.split('\n')
    filtered = filter(len, splited)
    input_type, filtered = filtered[0], filtered[1:]
    if input_type.upper() in ['H', 'HOR', 'HORIZONTAL']:
        inverted = [re.sub(r'\s+', '', s).split('|') for s in filtered]
        return itertools.izip(*inverted)
        # return (s[::-1] for s in itertools.izip(*inverted))
    else:
        raise Exception('Invalid type %s' % input_type)


def load_field_by_json(path):
    with open(path) as f:
        raw_txt = f.read()
    return field.Field.load_by_json(raw_txt)