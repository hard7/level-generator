from generator.spear_generator import SpearGenerator
from x_field import Field
from solver import solve, path_to_str
import pickle


def make():
    def make_one(i):
        field = gen.make_field()
        name = 'spear_%i' % i
        out = open('gen_spear/%s.txt' % name, 'w')
        out.write(field.take_json(name))
        out.close()

    gen = SpearGenerator((6, 6))
    map(make_one, xrange(50))


def compare():
    with open('dumps/x_field.dump') as file:
        a = pickle.load(file)

    with open('/ExternalLevels/s.txt') as file:
        b = Field.load_by_file(file)

    assert isinstance(a, Field)
    assert isinstance(b, Field)

    print 'a', len(solve(a))
    print 'b', len(solve(b))

    print a.take_text()
    print b.take_text()

if __name__ == '__main__':
    compare()

    # gen = SpearGenerator((6, 6))
    # x_field = gen._make_field()
    # with open('/ExternalLevels/s.txt', 'w') as f:
    #     f.write(x_field.take_json('s'))
    #
    # with open('x_field.dump', 'w') as f:
    #     pickle.dump(x_field, f)
    #
    # print '---'
    #
    # with open('/ExternalLevels/s.txt') as f:
    #     field2 = Field.load_by_file(f)
    #
    # print field2.take_text()
    # ans = solve(field2)
    #
    # print len(ans)
    # for a in ans:
    #     print path_to_str(a)