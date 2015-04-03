from bitarray import bitarray
from itertools import *
from timer import Timer
from random import *
from operator import itemgetter
from copy import *
from utils import *
import operator


x = set([1, 4])
y = set([1, 2, 4, 7, 9])
z = set([2, 3, 4, 7, 8, 9])

print 'z&y&x', z&y&x
print 'z&y', z&y
print 'z&y-x', z&y-x
print 'z-y-x', z-y-x



