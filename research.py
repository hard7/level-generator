import itertools
from collections import *
from itertools import *
from functools import partial
from random import *
import numpy as np
from timer import Timer
import pickle


from bitarray import bitarray


b0 = bitarray(100)
b0.setall(False)

b1 = bitarray(100)
b1.setall(False)
b1[5] = True

print b0 & b1