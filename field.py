__author__ = 'anosov'

from danger import Type, Dir, Danger

class Field:
    def __init__(self, x, y):
        self._dim_x, self._dim_y = x, y
        self._danger_cells = []
        self._danger_objects = []
        self._blocker_cells = []
        self._start = None
        self._finish = None
        self._time = None

    def add_object(self, coord, type_, periods=None, dirs=None):
        if type_ == Type.HERO:
            self._start = coord
        elif type_ == Type.FINISH:
            self._finish = coord
        elif type_ == Type.BRICK:
            self._blocker_cells.append(coord)
        elif type_ == Type.SPEAR:
            danger = Danger(coord, type_, periods)
            self._danger_objects.append(danger)
        elif type_ == Type.LASER:
            danger = Danger(coord, type_, periods, dirs)
            self._danger_objects.append(danger)
            self._blocker_cells.append(coord)

    def get_finish(self):
        return self._finish

    def get_start(self):
        return self._start

    def set_time(self, time):
        if self._time == time:
            return

        self._time = time
        self._danger_cells = []
        for danger in self._danger_objects:
            self._danger_cells.extend(danger.pull(time))

    @property
    def dim(self):
        return (self._dim_x, self._dim_y)

    def available_cells(self, coord):
        blocker = self._blocker_cells
        danger = self._danger_cells
        result = []
        for dir_ in Dir.ALL:
            ofs = Dir.move(coord, dir_)
            if self._in_range(ofs) and ofs not in blocker and ofs not in danger:
                result.append(ofs)
        return result

    def _in_range(self, coord):
        x, y = coord
        return (x >= 0) and (x <= self._dim_x-1) and (y >= 0) and (y <= self._dim_y-1)

    def init(self):
        for danger in self._danger_objects:
            if danger.type == Type.SPEAR:
                danger.danger_cells.append(danger.coord)

            elif danger.type == Type.LASER:
                for dir_ in danger.dirs:
                    coord = danger.coord
                    while not self._is_blocker(Dir.move(coord, dir_)):
                        coord = Dir.move(coord, dir_)
                        danger.danger_cells.append(coord)

    def is_valid(self):
        self.set_time(0)
        return self._start not in self._danger_cells

    def _is_blocker(self, coord):
        return coord in self._blocker_cells or not self._in_range(coord)


if __name__ == '__main__':
    field = Field(8, 5)
    field.add_object((2, 3), Type.HERO)
    field.add_object((2, 2), Type.BRICK)
    field.add_object((1, 1), Type.LASER, (1, 1, 1), [Dir.UP])

    field.init()
    field.set_time(0)
    print field.available_cells(field.get_start())