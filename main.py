__author__ = 'anosov'

from generator import Generator
from solver import Solver
import sys

path_to_levels = 'result/levels/'
answer_path = 'result/answer.txt'

if __name__ == '__main__':
    gen = Generator((4, 5), (4, 5))
    gen.set_range_filling(30, 50)
    count = 0
    # answer = open(answer_path, 'w')
    while count < 10:
        f = gen.make_field()
        s = Solver(f)
        cells = f.dim[0] * f.dim[1]
        res = s.run()
        if res and len(res)-1 >= 10 and len(res)-1 <= 16:
            print res
            print f.to_string()

            # name = "GenLevel_%i" % count
            # file = open(path_to_levels + name + '.txt', 'w')
            # file.write(f.to_string(name))
            # file.close()
            # answer.write("%s <%i> %s\n" % (name, len(res)-1, res,))
            count += 1
            # print count
    # answer.close()

