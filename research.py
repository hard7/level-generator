from bitarray import bitarray
from itertools import *
from timer import Timer
from random import *
from operator import itemgetter
from copy import *



class A:
    def __iter__(self):
        for i in [1, 2, 3]:
            yield i

    def next(self):
        d = next(self.c)
        return d


for a in A():
    print a