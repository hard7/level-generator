from itertools import chain, count
from collections import defaultdict
from bitarray import bitarray
bitarray.__hash__ = lambda s: hash(s.to01())
count_values = lambda t: t.count(1)


def BFS(danger_cells, n):
    def to_map(args):
        di, danger = args
        print '\ndi', di
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
                    else:
                        if len(di_map_pushed) + 1 < len(di_map[union]):
                            di_map[union] = di_map[pushed] + [di]
                            vi_map[union] = vi_map[pushed] + [vi]

            print variant.to01()
            print [(g.to01(), gg) for g, gg in di_map.iteritems()]

    en = enumerate
    di_map = defaultdict(list)
    vi_map = defaultdict(list)
    map(to_map, en(danger_cells))
    full = B('1')*n
    return zip(di_map[full], vi_map[full])


B = bitarray
if __name__ == '__main__':
    ds = '00100 00110', '01000 00100', '00010 10110 10001', '01111 00001'
    danger_cells = [map(B, d.split()) for d in ds]
    res = BFS(danger_cells, 5)
    print res

