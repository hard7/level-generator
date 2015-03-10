import random_coord


class Generator(object):
    def __init__(self, dim):
        self.dim = dim
        self.cell_count = dim[0] * dim[1]
        r = random_coord.UniqueRandomCoord
        self.random_coord = r(*dim)

    def make_field(self, prop=None):
        msg = 'Method Generator.make_field is pure virtual'
        raise NotImplementedError(msg)

