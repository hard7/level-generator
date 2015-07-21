__author__ = 'anosov'

from field import Field
from itertools import combinations, count, chain, ifilterfalse
import danger
import operator as op
from collections import defaultdict
from functools import partial
import fn


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

    def is_leaf(self):
        return bool(self.children)



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

        # self._root = field.start
        # root = Node(None, self._root)
        self.root = Node(None, field.start)
        self.cursor_nodes = [self.root]
        self.win_paths = []
        self._win_nodes = []
        self.field.init()
        self.move_count = 0
        self.leafs = []

        self._traveled_path = dict()  # of tuple of coordinates
        self._traveled_path[self.root] = (self.root.coord, )

    def run(self, t=1):
        assert t < 100
        future_leafs = []
        avc = self.field.available_for_move
        # not_in_path = lambda arg: arg not in cur.path()
        # is_not_in_path = lambda arg: arg not in self._traveled_path[cur]

        self.field.set_time(t)
        for cur in self.cursor_nodes:
            # available_coords = filter(is_not_in_path, avc(cur.coord))

            contains = partial(op.contains, self._traveled_path[cur])  # op.contains(a, b) some as: b in a
            available_coords = ifilterfalse(contains, avc(cur.coord))

            children = [Node(cur, c) for c in available_coords]
            cur.children = children
            future_leafs.extend(children)
            self.move_count += len(children)

            for child in children:
                self._traveled_path[child] = self._traveled_path[child.parent] + (child.coord, )

            if not children:
                self.leafs.append(cur)

        self.cursor_nodes = []
        for future_leaf in future_leafs:
            if future_leaf.coord == self.field.finish:
                # self.win_paths.append(future_leaf.path())
                self.win_paths.append(self._traveled_path[future_leaf])

                self._win_nodes.append(future_leaf)
                self.leafs.append(future_leaf)
            else:
                self.cursor_nodes.append(future_leaf)

        if self.cursor_nodes:
            return self.run(t+1)
        else:
            return self.win_paths

    def make_dict_of_path_lens(self):
        ways = defaultdict(list)
        # for leaf in self.leafs:
        #     n = lambda c=count(): c.next()
        #     ways[leaf].append(n())
        #     node = leaf.parent
        #     while node:
        #         ways[node].append(n())
        #         node = node.parent

        for leaf in self.leafs:
            ways[leaf.coord] = list()
            path = self._traveled_path[leaf.parent]
            for i, cell in enumerate(reversed(path), start=1):
                ways[cell].append(i)

        [var.sort() for var in ways.itervalues()]
        return ways

    def alternative_path_lens(self):
        ways = self.make_dict_of_path_lens()
        wpath = list()
        node = self._win_nodes[0]
        while node:
            wpath.append(node)
            node = node.parent

        wpath = fn.iters.pairwise(wpath[::-1])
        result = list()
        for parent_node, child_node in wpath:
            other_paths = ways[parent_node][:]
            [other_paths.remove(s+1) for s in ways[child_node]]
            result.append(tuple(other_paths))
        return tuple(result)

    def is_valid(self):
        apl = self.alternative_path_lens()
        print max(*chain(apl)) > 5

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

def solve_one(field):
    return Solver(field).run()[0]

