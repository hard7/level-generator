__author__ = 'anosov'
import collections


class Coord:
    def __init__(self, *args):
        _args = None
        if not args:
            _args = (0, 0)
        elif len(args) == 1:
            if isinstance(args[0], int):
                _args = args[0], args[0]
            elif isinstance(args[0], collections.Iterable):
                _args = args[0]
        elif len(args) == 2:
            _args = args
        self.y, self.x = _args

    def __hash__(self):
        return hash(self.dat)

    def __str__(self):
        return '.(%i, %i)' % self.dat

    def __repr__(self):
        return str(self)

    def __neg__(self):
        return Coord(-self.y, -self.x)

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.y + other.y, self.x + other.x)
        elif isinstance(other, int):
            return self + Coord(other)
        else:
            raise ArithmeticError('Unknown type %s' % type(other))

    def __sub__(self, other):
        tmp = -other
        return self + tmp

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if isinstance(other, Coord):
            return Coord(self.y * other.y, self.x * other.x)
        elif isinstance(other, int):
            return self * Coord(other)
        else:
            raise ArithmeticError('Unknown type')

    def __rmul__(self, other):
        return self * other

    def reset(self, other):
        self.x = other.x
        self.y = other.y
        return self

    def __div__(self, other):
        if isinstance(other, Coord):
            return Coord(self.y / other.y, self.x / other.x)
        elif isinstance(other, int):
            return self / Coord(other)
        else:
            raise ArithmeticError('Unknown type')

    def __rdiv__(self, other):
        if isinstance(other, Coord):
            return Coord(other.y / self.y, other.x / self.x)
        elif isinstance(other, int):
            return Coord(other) / self
        else:
            raise ArithmeticError('Unknown type')

    def __eq__(self, other):
        return self.y == other[0] and self.x == other[1]

    @property
    def dat(self):
        return self.y, self.x

    def copy(self):
        return Coord(self.dat)

    def __getitem__(self, item):
        return self.dat[item]

    def __setitem__(self, key, value):
        if key == 0: self.y = value
        elif key == 1: self.x = value
        else: raise Exception

    def __iter__(self):
        return iter(self.dat)