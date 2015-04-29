__author__ = 'anosov'
import load
import init
import itertools
import solver


def show_invalid_ascii_fields(path):
    c = itertools.count()
    invalid = list()
    for ascii in load.load_template_ascii_gen_from_file(path):
        cur = c.next()
        try:
            init.init_template_field_by_ascii(ascii)
        except AssertionError:
            invalid.append(cur)
    print 'Invalid ascii fields:', invalid


def show_path_count_for_fields(fields):
    print 'Path count for fields:',
    for field in fields:
        print len(solver.solve(field)),
    print
