import operator
import random
import itertools


def _getattr(name, default=None):
    return lambda obj: getattr(obj, name, default)


def _getitem(index):
    return lambda obj: operator.getitem(obj, index)


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
    item = random.choice(array)
    array.remove(item)
    return item

