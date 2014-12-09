__author__ = 'anosov'

from danger import Type, Dir, Danger
import string

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

    def to_string(self, name='noname'):
        str = ''
        str += name + '\n'
        str += "%i %i" % (self._dim_x, self._dim_y)
        front_index, back_index = 0, 25
        index = 0
        postfix = ''
        art = [['.' for _ in xrange(self._dim_x)] for _ in xrange(self._dim_y)]
        for x, y in self._blocker_cells:
            art[y][x] = '#'
        for dang in self._danger_objects:
            x, y = dang.coord
            if dang.type == Type.LASER:
                art[y][x] = string.ascii_uppercase[front_index]
                on, off, offset = dang.on_period, dang.off_period, dang.offset
                flag = 'on' if offset < on else 'off'
                postfix += '%s:laser %s %s %i %i %i \n' % \
                           (art[y][x], self._dirs_to_string(dang.dirs), flag, on, off, offset % on)
                index += 1
                front_index += 1
            elif dang.type == Type.SPEAR:
                art[y][x] = string.ascii_uppercase[back_index]
                on, off, offset = dang.on_period, dang.off_period, dang.offset
                offset_ = offset if offset < on else offset - on
                flag = 'on' if offset < on else 'off'
                postfix += '%s:spear %s %i %i %i \n' % \
                           (art[y][x], flag, on, off, offset_)
                index += 1
                back_index -= 1
        x, y = self._start
        art[y][x] = 's'

        x, y = self._finish
        art[y][x] = 'f'

        str += '\n'
        str += '%s \n' % '\n'.join([''.join(row) for row in art][::-1])
        str += '%i \n' % index
        str += '%s \n' % postfix
        return str

    def _dirs_to_string(self, dirs):
        conv = {Dir.UP: 'u', Dir.LEFT: 'l', Dir.DOWN: 'd', Dir.RIGHT: 'r'}
        return ''.join([conv[dir_] for dir_ in dirs])

    def trace(self):
        print 'dim: ', self._dim_x, self._dim_y
        print '_blocker_cells', self._blocker_cells
        for dan in self._danger_objects:
            print 'Danger %i (%i %i %i)' % (dan.type,
                dan.on_period,
                dan.off_period,
                dan.offset)
            print dan.dirs
            print dan.danger_cells



if __name__ == '__main__':
    field = Field(8, 5)
    field.add_object((2, 3), Type.HERO)
    field.add_object((2, 2), Type.BRICK)
    field.add_object((1, 1), Type.LASER, (1, 1, 1), [Dir.UP])

    field.init()
    field.set_time(0)
    print field.available_cells(field.get_start())