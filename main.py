import scripts
import solver
import field

if __name__ == '__main__':
    # gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    # fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    # g = scripts.calc_covered_gen(fields[0])
    # f = g.next()

    dump = '../x.dmp'
    import pickle
    with open(dump, 'r') as _file:
        f = pickle.load(_file)

    s = solver.Solver(f)
    s.run()
    s.count_ways()

def act():
    gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    fields = fields[:1]

    scripts.show_path_count_for_fields(fields)
    g = scripts.calc_covered_gen(fields[0])

    while not raw_input('>'):
        scripts.save_fields2out([g.next()], '/ExternalLevels', 'lev')





