import operator
import random
import itertools
import contextlib


def _getattr(name, default=None):
    return lambda obj: getattr(obj, name, default)


class xgetitem:
    class _(type):
        def __getitem__(cls, item):
            return cls(idx=item)

        def __call__(self, idx=None, obj=None):
            assert (idx is None) ^ bool(obj is None)
            if idx: return lambda object: operator.getitem(object, idx)
            elif obj: return lambda index: operator.getitem(obj, index)
    __metaclass__= _

xget = xgetitem

def mrun(func_name, *args):
    def wrap(obj):
        func = getattr(obj, func_name)
        return func(*args)
    return wrap

xrun = mrun

def xgetattr(attr):
    def wrap(obj):
        return getattr(obj, attr)
    return wrap


def elvis(obj, default):
    return obj if obj else default

@contextlib.contextmanager
def nested_break_contextmanager():
    class NestedBreakException(Exception):
        pass
    try:
        yield NestedBreakException
    except NestedBreakException:
        pass



def take_some(array, indexes):
    return [array[index] for index in indexes if index < len(array)]

def gen_some(array, indexes):
    for index in indexes:
        if index < len(array):
            yield array[index]

def get_reflection(dim, coord):
    x, y = dim
    cx, cy = coord
    return x-cx-1, y-cy-1


choice_from_set = lambda l: random.sample(l, 1)[0]


def choice_and_pop(array):
    if not array:
        return None

    _choice = None
    if isinstance(array, set):
        _choice = choice_from_set
    elif isinstance(array, list):
        _choice = random.choice
    item = _choice(array)
    array.remove(item)
    return item

