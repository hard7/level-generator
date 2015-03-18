__author__ = 'anosov'

from random import randrange, choice

from danger_field import Type, Dir
from field import Field
from random_coord import UniqueRandomCoord
from generator import Generator
from copy import copy

class EasyGenerator(Generator):
    FILLED = 1
    HERO_AND_FINISH = 2

    def __init__(self, x_coord, y_coord):
        super(EasyGenerator, self).__init__(x_coord, y_coord)

    def make_field(self, type_=FILLED):
        if type_ == EasyGenerator.FILLED:
            return self._make_field()
        elif type_ == EasyGenerator.HERO_AND_FINISH:
            return self._make_field_hf()

    def reflection_coord(self, coord):
        return self.x_coord - coord[0] - 1, self.y_coord - coord[1] - 1

    def _make_field(self):
        field = None
        while not field or not field.is_valid():
            self.random_coord.clear()
            field = Field(self.x_coord, self.y_coord)
            hero_coord = self.random_coord.get_on_border()
            finish_coord = self.random_coord.get_reflection(hero_coord)

            field.add_object(hero_coord, Type.START)
            field.add_object(finish_coord, Type.FINISH)

            cell_count = float(self.x_coord * self.y_coord)
            fill = (30, 50)             # self._filling_range
            range_ = (cell_count * fill[0] / 100, cell_count * fill[1] / 100)
            range_ = (int(range_[0]-2), int(range_[1]-2)+1)
            object_count = randrange(*range_)
            funcs = [self._make_laser, self._make_spear, self._make_brick]
            for _ in range(object_count):
                f = choice(funcs)
                args = f()
                field.add_object(self.random_coord.get_any(), *args)
            field.init()

        return field

    def _make_field_hf(self):
        field = Field(self.x_coord, self.y_coord)

        # hero_coord = self.random_coord.get_on_border
        # finish_coord = (self.x_coord-1-hero_coord[0], self.y_coord-1-hero_coord[1])
        #
        # field.add_object(hero_coord, Type.HERO)
        # field.add_object(finish_coord, Type.FINISH)

        return field

    _make_laser = lambda self: (Type.LASER, self._make_periods(), self._make_dirs())
    _make_spear = lambda self: (Type.SPEAR, self._make_periods())
    _make_brick = lambda self: (Type.BRICK, None)

    def _make_periods(self):
        on, off = randrange(1, 4), randrange(1, 4)
        return on, off, randrange(on+off)

    @staticmethod
    def _make_dirs():
        res = list(Dir.ALL)
        for i in range(randrange(3+1)):
            res.remove(choice(res))
        return res

