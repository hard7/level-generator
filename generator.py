__author__ = 'anosov'

from danger import Type, Dir
from field import Field
from random import randrange, choice


class Generator:
    def __init__(self, x_range, y_range):
        self._x_range = x_range
        self._y_range = y_range
        self._range_filling = None
        self._filled_cells = None
        self._x = None
        self._y = None

    def set_range_filling(self, x, y):
        self._range_filling = (x, y)

    @property
    def rand_coord(self):
        # print self._x * self._y, len(self._filled_cells)
        if len(self._filled_cells) == (self._x * self._y):
            input("PRESS ENTER TO CONTINUE.")
            raise Exception('full _filled_cells')
        while True:
            coord = (randrange(self._x), randrange(self._y))
            if coord not in self._filled_cells:
                self._filled_cells.append(coord)
                return coord

    def rand_coord_on_border(self):
        fix = randrange(2)
        dim = (self._x, self._y)
        z = [choice([0, dim[fix]-1]), randrange(dim[1 - fix])]
        return tuple(z[::-fix*2+1])

    def gen_dim(self):
        self._x, self._y = randrange(*self._x_range), randrange(*self._y_range)

    def make_field(self):
        self.gen_dim()
        field = None
        while not field or not field.is_valid():
            self._filled_cells = []
            field = Field(self._x, self._y)

            # field.add_object(self.rand_coord, Type.HERO)
            # field.add_object(self.rand_coord, Type.FINISH)

            hero_coord = self.rand_coord_on_border()
            finish_coord = (self._x-1-hero_coord[0], self._y-1-hero_coord[1])

            field.add_object(hero_coord, Type.HERO)
            field.add_object(finish_coord, Type.FINISH)

            self._filled_cells.extend([hero_coord, finish_coord])

            cell_count = float(self._x * self._y)
            fill = self._range_filling
            range_ = (cell_count * fill[0] / 100, cell_count * fill[1] / 100)
            range_ = (int(range_[0]-2), int(range_[1]-2)+1)
            object_count = randrange(*range_)
            funcs = [self._make_laser, self._make_spear, self._make_brick]
            for _ in range(object_count):
                # print len(self._filled_cells), '/', self._x * self._y, '--', _
                args = choice(funcs)()
                # print _, args
                field.add_object(self.rand_coord, *args)
            field.init()
        return field

    def _make_laser(self):
        return tuple((Type.LASER, self._make_periods(), self._make_dirs()))

    def _make_spear(self):
        return tuple((Type.SPEAR, self._make_periods()))

    def _make_brick(self):
        return tuple((Type.BRICK, None))

    def _make_periods(self):
        on, off = randrange(1, 4), randrange(1, 4)
        return tuple((on, off, randrange(on+off)))

    def _make_dirs(self):
        res = []
        count = randrange(1, 5)
        while len(res) != count:
            dir_ = choice(Dir.ALL)
            if dir_ not in res:
                res.append(dir_)
        return res

if __name__ == '__main__':
    gen = Generator((3, 8), (3, 8))
    gen.set_range_filling(40, 70)

    # for _ in range(20):
    #     field = gen.make_field()
