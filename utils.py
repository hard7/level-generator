import operator


def _getattr(name, default=None):
    return lambda obj: getattr(obj, name, default)


def _getitem(index):
    return lambda obj: operator.getitem(obj, index)


def take_some(array, indexes):
    return [array[index] for index in indexes if index < len(array)]


def get_reflection(dim, coord):
    x, y = dim
    cx, cy = coord
    return x-cx-1, y-cy-1