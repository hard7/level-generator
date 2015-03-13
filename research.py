import itertools
from collections import *
from itertools import *
from functools import partial
from random import *
import numpy as np
from timer import Timer
import pickle
from sys import getsizeof as sizeof

from bitarray import bitarray


b0 = bitarray('01001')
# b0.setall(False)

z0 = bitarray('01001')
# z.setall(False)

b1 = bitarray('11010111011')
# b1.setall(False)
# b1[5] = True

s = set([b0, b1])
l = list([b0, b1])

print b1 in s
print z0 in s

print b1 in l
print z0 in l

print z0 == b0
print [z0 == i for i in l]
