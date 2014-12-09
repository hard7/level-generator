__author__ = 'anosov'

from field import Field


class Node:
    def __init__(self, parent, coord):
        self.parent = parent
        self.children = None
        self.coord = coord


class Solver:
    def __init__(self, field):
        self._field = field
        self._root = field.get_start()


        root = Node(None, field.get_start())
        self._open_branches = [root]
        self._graph = [root]

        self._time = 0
        self._target = field.get_finish()

    def run(self):
        while True:
            self._next_step()
            if not self._open_branches:
                # print 'fail', self._time
                return None

            target = [o for o in self._open_branches if o.coord == self._target]
            if target:
                return list(reversed(self._path(target[0])))

    def _next_step(self):
        next_open = []
        self._time += 1
        self._field.set_time(self._time)
        for open_ in self._open_branches:
            result = self._field.available_cells(open_.coord)
            path = self._path(open_)
            nodes = [Node(open_, coord) for coord in result if coord not in path]
            open_.children = nodes
            next_open.extend(nodes)
        self._open_branches = next_open

    def _path(self, node):
        res = [node.coord]
        while node.parent:
            node = node.parent
            res.append(node.coord)
        return res


from generator import Generator


