import itertools
from itertools import *
from functools import partial
from random import *
from collections import defaultdict
from timer import Timer
from operator import itemgetter, attrgetter, methodcaller
import pickle
from bitarray import bitarray
bitarray.__hash__ = lambda s: hash(s.to01())


def make_ticket():
    _count = randrange(1, 10)
    ticket = bitarray('0') * 100
    for _ in xrange(_count):
        ticket[randrange(100)] = True
    return ticket

def make_chest():
    _count = randrange(1, 10)
    return [make_ticket() for _ in xrange(_count)]


matches = defaultdict(set)
indexes_i = dict()
indexes_j = dict()
indexes_k = dict()
indexes = dict()


def iteration(args):
    j, chest = args
    c0, c1 = count(), count()

    added = defaultdict(set)
    for i, ticket in enumerate(chest):
        idx = ticket.count(1)
        if ticket not in added[idx]:
            added[idx].add(ticket)
            indexes[ticket] = [(j, i), ticket]
            # indexes_i[ticket] = i
            # indexes_j[ticket] = j
            # indexes_k[ticket] = None
            c0.next()
        else:
            c1.next()

    for i, ticket in enumerate(chest):
        for item in chain(*matches.itervalues()):
            union = ticket | item
            idx = union.count(1)

            if union not in added[idx] and union not in matches[idx]:
                added[idx].add(union)
                indexes_i[union] = i
                indexes_j[union] = j
                indexes_k[union] = ticket
                c0.next()
            else:
                c1.next()

    for i, val in added.iteritems():
        matches[i].update(val)

    print '\t\t\t\t\t\t\tins/skip/items', c0.next()-1, c1.next()-1, sum(map(len, matches.itervalues()))

# chests = [make_chest() for _ in xrange(50)]
# with open('dump_bit.txt', 'w') as f:
#     pickle.dump(chests, f)
# exit()

with open('dump_bit.txt') as f:
    chests = pickle.load(f)


# for chest in chests:
#     for i, ticket in enumerate(chest):
#         bar = bitarray(100)
#         bar.setall(0)
#         for item in ticket:
#             bar[item] = 1
#         chest[i] = bar

def run(n):
    with Timer('ALL'):
        for j, chest in enumerate(chests):
            with Timer('iter %i' % j) as t:
                iteration((j, chest))
                if j == n:
                    break
    print matches.keys()[-1]

import pstats
import cProfile
import re


run(5)

# cProfile.scripts('scripts()', '_restats')
# p = pstats.Stats('_restats')
# p.strip_dirs()
# p.sort_stats('time', 'cumulative')
# p.print_stats()


# cc, nc, tt, ct, callers