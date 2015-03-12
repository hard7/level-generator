import itertools
from itertools import *
from functools import partial
from random import *

def make_ticket():
    _count = randrange(1, 10)
    return set([randrange(100) for _ in xrange(_count)])

def make_chest():
    _count = randrange(1, 10)
    return [make_ticket() for _ in xrange(_count)]

chests = [make_chest() for _ in xrange(50)]

matches = [[] for _ in xrange(100)]


def iteration():
    for match in matches:
        pass


en = enumerate
for j, chest in en(chests):
    for i, ticket in en(chest):
        iteration()

print map(len, matches)

