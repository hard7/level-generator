__author__ = 'anosov'

from x_field import Field
from itertools import combinations
import danger
import operator as op

class Node:
    def __init__(self, parent, coord):
        self.parent = parent
        self.children = None
        self.coord = coord

    def path(self):
        node = self
        path = [node.coord]
        while node.parent:
            node = node.parent
            path.append(node.coord)
        return path[::-1]


def find_passed_cells(paths):
    passed = {}
    for path_count, path in enumerate(paths):
        for step_count, coord in enumerate(path):
            if coord not in passed:
                passed[coord] = []
            passed[coord].append(path_count)
    return passed


def find_option(passed_cells):
    res = {}
    for key, values in passed_cells.iteritems():
        res[key] = set(combinations(values, 3))
    return res

def find_paths_to_finish(field):
    return Solver(field).run()


def find_crossing_cells(paths, indexes=None):
    if indexes:
        paths = [paths[i] for i in indexes]
    return list(reduce(lambda res, x: set(res)-set(x), paths))


class Solver(object):
    def __init__(self, field):
        assert isinstance(field, Field)
        self.field = field
        self._root = field.start
        root = Node(None, self._root)
        self._leafs = [root]
        self.win_paths = []
        self.field.init()

    def run(self, t=1):
        assert t < 100
        future_leafs = []
        avc = self.field.available_for_move
        not_in_path = lambda arg: arg not in leaf.path()
        self.field.set_time(t)
        for leaf in self._leafs:
            available_coords = filter(not_in_path, avc(leaf.coord))
            children = [Node(leaf, c) for c in available_coords]
            leaf.children = children
            future_leafs.extend(children)

        self._leafs = []
        for future_leaf in future_leafs:
            if future_leaf.coord == self.field.finish:
                self.win_paths.append(future_leaf.path())
            else:
                self._leafs.append(future_leaf)

        if self._leafs:
            return self.run(t+1)
        else:
            return self.win_paths


def path_to_str(path):
    char = dict(zip(danger.Dir.ALL, 'URDL'))
    base = None
    result = ''
    for i, coord in enumerate(path):
        if not base:
            base = coord
            continue
        dir = tuple(map(op.sub, coord, base))
        result += char[dir]
        if i and i % 3 == 0:
            result += ' '
        base = coord
    return result


def solve(field):
    return Solver(field).run()