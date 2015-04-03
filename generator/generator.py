import random_coord


class Generator(object):
    def __init__(self, *args):
        self.dim = args[0] if len(args) == 1 else args[:2]
        self.cell_count = self.dim[0] * self.dim[1]
        r = random_coord.UniqueRandomCoord
        self.random_coord = r(*self.dim)

    def make_field(self, prop=None):
        msg = 'Method Generator.make_field is pure virtual'
        raise NotImplementedError(msg)

