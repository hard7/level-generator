__author__ = 'anosov'
from lazy import lazy
import solver
import scripts
from copy import deepcopy
import fn
from fn import _, F
from timer import Timer

class DataProcessing(object):
    def __init__(self, field, covers):
        self.field = field
        self.covers = covers

    @lazy
    def solver(self):
        with Timer('solver'):
            run = F(deepcopy) >> solver.Solver >> [_.call('run')] and fn._
            return map(run, scripts.covered(self.field, self.covers))

    @lazy
    def len_path(self):
        with Timer('len_path'):
            return map(_.win_paths[0], self.solver)

    @lazy
    def alternative_path_len(self):
        with Timer('alternative_path_len'):
            return map(_.call('alternative_path_lens'), self.solver)

    @lazy
    def walked_spear(self):
        with Timer('walked_spear'):
            path = lambda solver: set(solver.win_paths[0])
            spear = lambda solver: set(solver.field.get_spear_coords())
            return [len(path(s) & spear(s)) for s in self.solver]


class A:
    def __init__(self):
        self.var = {1: 'azaza'}


# print map(_.var.values(), [A()])

