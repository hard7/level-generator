from itertools import chain, count
from collections import defaultdict
from bitarray import bitarray
bitarray.__hash__ = lambda s: hash(s.to01())
count_values = lambda t: t.count(1)


def make_item(arr, n):
    item = bitarray('0')*n
    for i in arr:
        item[i] = True
    return item


def BFS(danger_cells, n):
    def to_map(args):
        di, danger = args
        print 'di', di, '/', len(danger_cells)
        for vi, variant in en(danger):
            di_map[variant] = [di]
            vi_map[variant] = [vi]

            for pushed in di_map.keys():
                di_map_pushed = di_map[pushed]
                if di not in di_map_pushed:
                    union = pushed | variant
                    if union not in di_map:
                        di_map[union] = di_map_pushed + [di]
                        vi_map[union] = vi_map[pushed] + [vi]
                    elif len(di_map_pushed) + 1 < len(di_map[union]):
                        di_map[union] = di_map_pushed + [di]
                        vi_map[union] = vi_map[pushed] + [vi]

            # print variant.to01()
            # print [(g.to01(), gg) for g, gg in di_map.iteritems()]

    en = enumerate
    di_map = dict()
    vi_map = dict()

    map(to_map, en(danger_cells))
    res = [k for k in di_map.iterkeys() if k.count(True) == n]
    res = [(r.to01(), zip(di_map[r], vi_map[r])) for r in res]
    # res[1:] = res[1:]
    return res

if __name__ == '__main__':
    bs = '0101 0001', '1001 0100', '0100 1100 0010', '0011'
    bs = [map(bitarray, b.split()) for b in bs]
    res = BFS(bs, 3)
    print '>', res