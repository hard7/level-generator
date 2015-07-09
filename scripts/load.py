__author__ = 'anosov'
import re
import itertools
import field
import utils


def load_template_ascii_gen_from_file(path):
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


def str_file_to_one_json_field(raw, start_signs='sSoO', finish_signs='fF^', wall_signs='xX#', empty_signs='.'):
    all_signs = start_signs + finish_signs + wall_signs + empty_signs
    assert utils.all_items_is_unique(all_signs)
    assert ' ' not in all_signs
    assert isinstance(raw, str)

    raw_without_spaces = raw.strip()
    splited = raw_without_spaces.split('\n')

    raise NotImplementedError

    # assert map(len, splited)
    #
    # print splited