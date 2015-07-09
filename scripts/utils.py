__author__ = 'anosov'


def all_items_is_unique(array):
    seen = set()
    return not any(i in seen or seen.add(i) for i in array)
