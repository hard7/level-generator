import itertools
from itertools import *
from functools import partial
from random import *
from collections import defaultdict
from timer import Timer
from operator import itemgetter, attrgetter, methodcaller
import pickle


def make_ticket():
    _count = randrange(1, 10)
    return frozenset([randrange(100) for _ in xrange(_count)])

def make_chest():
    _count = randrange(1, 10)
    return [make_ticket() for _ in xrange(_count)]


matches = defaultdict(set)
indexes_i = dict()
indexes_j = dict()
indexes_k = dict()

def iteration(args):
    j, chest = args
    c0, c1 = count(), count()

    added = defaultdict(set)
    for i, ticket in enumerate(chest):
        idx = len(ticket)
        if ticket not in added[idx]:
            added[idx].add(ticket)
            # indexes[ticket] = [(j, i)]
            indexes_i[ticket] = i
            indexes_j[ticket] = j
            indexes_k[ticket] = None
            c0.next()
        else:
            c1.next()


    for i, ticket in enumerate(chest):
        for item in chain(*matches.itervalues()):
            union = ticket | item
            idx = len(union)
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

    print '\t\t\t\t\t\t\tins/skip', c0.next()-1, c1.next()

def merge(a, b): return a | b


def mn(chest, ticket, added, j, i):
    for item in chain(*matches.itervalues()):
        mn2(ticket, item, added, j, i)

def mn2(ticket, item, added, j, i):
    item |= ticket
    # union = ticket | item
    idx = len(item)
    if mn3(item, added, idx):
        mn4(item, added, idx, ticket, (j, i))

def mn3(union, added, idx):
    return union not in added[idx] and union not in matches[idx]

def mn4(union, added, idx, ticket, (j, i)):
    if union not in added[idx] and union not in matches[idx]:
        mp5(added, idx, union, ticket, (j, i))

def mp5(added, idx, union, ticket, (j, i)):
    added[idx].add(union)
    mp6(union, ticket, (j, i))

def mp6(union, ticket, (j, i)):
    indexes_i[union] = i
    indexes_j[union] = j
    indexes_k[union] = ticket
    # indexes[union] = indexes[ticket][:]
    # indexes[union].append((j, i))

# chests = [make_chest() for _ in xrange(50)]
with open('dump.txt') as f, Timer('read chests'):
    chests = pickle.load(f)

def run():
    for j, chest in enumerate(chests):
        with Timer('iter %i' % j) as t:
            iteration((j, chest))
            if j == 10:
                break
    print matches.keys()[-1]

import pstats
import cProfile
import re

cProfile.run('run()', '/tmp/restats')
p = pstats.Stats('/tmp/restats')
p.strip_dirs()
p.sort_stats('time', 'cum')
p.print_stats()


# cc, nc, tt, ct, callers