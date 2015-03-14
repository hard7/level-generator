from generator.spear_generator import SpearGenerator


def make():
    def make_one(i):
        field = gen.make_field()
        name = 'spear_%i' % i
        out = open('gen_spear/%s.txt' % name, 'w')
        out.write(field.take_json(name))
        out.close()

    gen = SpearGenerator((6, 6))
    map(make_one, xrange(50))


if __name__ == '__main__':
    gen = SpearGenerator((6, 6))
    field = gen._make_field()