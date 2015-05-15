__author__ = 'anosov'

import solver
import fn
from fn import _
from lazy import lazy


class Mark(object):
    def __init__(self, impl, *ar, **kw):
        self.impl = impl
        self.args = ar
        self.kwarg = kw
        self.data_process = None
        self.factor = 1.
        self.result = list()

    def __mul__(self, num):
        self.factor *= num
        return self

    def run(self, dp):
        self.result = self.impl(dp, *self.args, **self.kwarg)


def len_path(data):
    assert isinstance(data, DataProcessing)


class DataProcessing(object):
    def __init__(self, field, covers):
        self.field = field
        self.covers = covers
        self.params = dict()

    def get(self, key, init, *ar, **kw):
        value = self.params.get(key)
        if value is None:
            value = self.params.setdefault(key, init(*ar, **kw))
        return value

    @property
    def len_path(self):
        def init():
            print 'init len path'
            return 42

        return self.get('len_path', init)

    @lazy
    def len_abs(self):
        print 'init len_abs'
        return 42

class CoverAnalyzer(object):
    def __init__(self, field, covers):
        self.data_process = DataProcessing(field, covers)
        self.marks = list()

    def run_marks(self):
        for mark in self.marks:
            mark.run(self.data_process)

    def analyze(self):
        self.run_marks()
        raise NotImplementedError


dp = DataProcessing(0, 0)
r = dp.len_path
r = dp.len_path

# itertools.ifilterfalse(lambda cn: isnan(cn[1]), cover_norm)
import math


# c = [(float('nan'), 1), (6., 2), (7., 3)]
# foo = fn.F() >> _[0] >> math.isnan >> 1 - _


# foo = fn.F() >> fn.op.call(math.isnan, _[0]) >> 1 - _
# foo = fn.F(math.isnan, _[0])
# bar = fn.F(fn.iters.filterfalse,
#
# print filter(foo, c)
#
# print (dp.__dict__)
