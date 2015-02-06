
from random import randrange, choice


def decorator_unique(fn):
    def wrapper_func(self, *args, **kwargs):
        assert isinstance(self, UniqueRandomCoord)
        coord_count = self.x_coord * self.y_coord
        assert len(self.returned) != coord_count

        while True:
            coord = fn(self, *args, **kwargs)
            if not self.coord_returned(coord):
                self.add_to_returned(coord)
                return coord

    return wrapper_func


class UniqueRandomCoord(object):
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.returned = []

    x_rand = lambda self: randrange(self.x_coord)
    y_rand = lambda self: randrange(self.y_coord)

    def clear(self):
        self.returned = []

    def coord_returned(self, coord):
        return coord in self.returned

    def add_to_returned(self, coord):
        assert not self.coord_returned(coord)
        self.returned.append(coord)

    def get_any_n(self, n):
        return [self.get_any() for _ in range(n)]

    def get_on_border_n(self, n):
        return [self.get_on_border() for _ in range(n)]

    @decorator_unique
    def get_any(self):
        return self.x_rand(), self.y_rand()

    @decorator_unique
    def get_on_border(self):
        fix = randrange(2)
        unfix = 1 - fix
        dim = (self.x_coord, self.y_coord)
        last = dim[fix]-1
        direct = 1-fix*2
        z = [choice([0, last]), randrange(dim[unfix])]
        return tuple(z[::direct])

    def get_reflection(self, (x, y)):
        rc = self.x_coord - x - 1, self.y_coord - y - 1
        self.add_to_returned(rc)
        return rc