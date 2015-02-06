__author__ = 'anosov'

import random
import solver


class PathFinder(object):
    def __init__(self, field):
        self.paths = solver.find_paths_to_finish(field)
        self.passed_cells = self._find_passed_cells(self.paths)

    def gen_next(self, pos, _min, _max):
        p = [len(p) for p in self.paths]
        # p = [1, 2, 3, 3, 3, 5, 6, 7, 8, 9, 9, 10, 11, 11, 14]
        for i in xrange(pos+1, len(p)):
            if _min <= abs(p[pos]-p[i]) <= _max:
                yield i

    def gen_triple(self, _min, _max):
        for i, _ in enumerate(self.paths):
            for j in self.gen_next(i, _min, _max):
                for k in self.gen_next(j, _min, _max):
                    yield i, j, k

    def make_triples(self, _min=2, _max=6):
        return [o for o in self.gen_triple(_min, _max)]

    @staticmethod
    def _find_passed_cells(paths):
        passed = {}
        for path_count, path in enumerate(paths):
            for step_count, coord in enumerate(path):
                if coord not in passed:
                    passed[coord] = []
                passed[coord].append(path_count)
        return passed

