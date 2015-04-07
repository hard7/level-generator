__author__ = 'anosov'
import field
import solver
import danger
import itertools
import operator
import random
import utils
from bitarray import bitarray
bitarray.__hash__ = lambda s: hash(s.to01())
bitarray.__repr__ = lambda s: s.to01()


def to_list(bitarr):
    e = enumerate
    return tuple(i for i, flag in e(bitarr) if not flag)


class Period(object):
    class PeriodType(type):
        def __new__(mcs, name, bases, _dict):
            p = itertools.product(range(1, 3+1), repeat=2)
            p = [map(lambda offset: (on, off, offset),
                     xrange(on+off)) for on, off in p]
            _dict['period'] = list(itertools.chain(*p))
            return type.__new__(mcs, name, bases, _dict)

        def __len__(cls):
            return len(getattr(cls, 'period'))

        def __getitem__(cls, item):
            return getattr(cls, 'period')[item]

        def index(cls, idx):
            return getattr(cls, 'period').index(idx)

        def __iter__(cls):
            for p in getattr(cls, 'period'):
                yield p
    __metaclass__ = PeriodType


class Cover(object):
    def __init__(self, period, intersection, path_count):
        self.period = period
        _as = danger.Danger.at_stake
        at_stake = lambda (path, idx): _as(period, idx)
        isec = filter(at_stake, intersection)
        cover = map(operator.itemgetter(0), isec)
        self._cover = Cover.make(cover, path_count)

    def index(self):
        return Period.index(self.period)

    def __nonzero__(self):
        return any(self._cover)

    def __call__(self):
        return self._cover

    @staticmethod
    def make(cover, _len):
        b = bitarray('0'*_len)
        [operator.setitem(b, c, 1) for c in cover]
        return b


class Spear(object):
    def __init__(self, coord, paths):
        self.coord = coord
        target_paths = filter(lambda p: coord in p, paths)
        isec = [(paths.index(path), path.index(coord)) for path in target_paths]
        self._covers = [Cover(per, isec, len(paths)) for per in Period]
        self._covers = filter(bool, self._covers)
        random.shuffle(self._covers)
        # print 'cover count', len(self._covers)

    def __nonzero__(self):
        return bool(self._covers)

    def choice_and_pop(self):
        return utils.choice_and_pop(self._covers)

    def pop_cover(self):
        return self._covers.pop()


class DField(object):

    def __init__(self, _field, requared_path_count=3, max_spear=10, max_answer=5000):
        assert isinstance(_field, field.Field)
        self._path_counts = [requared_path_count] \
            if isinstance(requared_path_count, int) \
            else requared_path_count
        self._cells = _field.free_cells[:]
        self._paths = solver.Solver(_field).run()
        self._spears = [Spear(cell, self._paths)
                        for cell in self._cells]
        random.shuffle(self._spears)
        self._left = map(id, self._spears)
        self._max_spear = max_spear
        self._answer_count = max_answer

        print '=> path count:', len(self._paths)
        print '=> cell count:', len(self._cells)
        # print 'period count', len(Period)

    def gen_spear(self):
        for spear in itertools.cycle(self._spears):
            if spear:
                yield spear
            elif id(spear) in self._left:
                self._left.remove(id(spear))
                if not self._left:
                    break

    def gen_cover(self):
        for spear in self.gen_spear():
            si = self._cells.index(spear.coord)
            cover = spear.pop_cover()
            yield cover(), si, cover.index()

    @property
    def paths(self):
        return self._paths

    def __iter__(self):
        self.cov = self.gen_cover()
        self.si_map = dict()
        self.ci_map = dict()
        self.counter = 0
        self.iter_count = itertools.count()
        return self

    def next(self):
        if self.counter > self._answer_count:
            raise StopIteration

        path_counts = self._path_counts
        cover, si, ci = self.cov.next()
        si_map, ci_map = self.si_map, self.ci_map
        si_map[cover] = [si]
        ci_map[cover] = [ci]
        answers = []
        for pushed in si_map.keys():
            si_map_pushed = si_map[pushed]
            if si not in si_map_pushed:
                union = pushed | cover
                answer_count = union.count(0)
                if union not in si_map:
                    if answer_count in path_counts:
                        res = (union, si_map_pushed, ci_map[pushed], si, ci)
                        answers.append(res)
                    if answer_count > min(path_counts) and len(si_map_pushed) < self._max_spear:
                        si_map[union] = si_map_pushed + [si]
                        ci_map[union] = ci_map[pushed] + [ci]
                elif len(si_map_pushed) + 1 < len(si_map[union]):
                    si_map[union] = si_map_pushed + [si]
                    ci_map[union] = ci_map[pushed] + [ci]
                    if answer_count in path_counts:
                        res = (union, si_map_pushed, ci_map[pushed], si, ci)
                        answers.append(res)

        res = self.collect_answers(answers)
        self.counter += len(res)
        print self.iter_count.next(), 'len si_map', len(si_map.keys()), self.counter
        return res

    def collect_answers(self, answers):
        def detail(prop):
            si, ci = prop
            return self._cells[si] + Period[ci]

        def collect(answer):
            paths = [self._paths[i] for i in to_list(answer[0])]
            props = zip(*answer[1:3]) + [answer[3:]]
            return paths, map(detail, props)
        return map(collect, answers)


if __name__ == '__main__':
    _field = field.Field((2, 3))
    _field.add_object((0, 0), field.Type.START)
    _field.add_object((1, 2), field.Type.FINISH)
    d = DField(_field)

    c = itertools.count()
    for i in d:
        c.next()
    print c.next()



