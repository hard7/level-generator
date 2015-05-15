__author__ = 'anosov'

import danger_field
import solver
import copy

def calc_covered_fields(fields, n):
    pass


def choice_good_covers(field, covers, n):
    paths = list()
    move_count = list()
    spear_walked = list()
    field.save_backup()
    fish_paths = solver.Solver(field).run()
    min_lfp, max_lfp = len(fish_paths[1]), len(fish_paths[-1])
    covers = list(covers)
    for i, cover in enumerate(covers):
        map(field.add_spear, cover)
        _solver = solver.Solver(field)
        path = _solver.run()[0]
        assert len(_solver.win_paths) == 1
        sw = len(set(field.get_spear_coords()) & set(path))
        paths.append(path)
        move_count.append(_solver.move_count)
        spear_walked.append(sw)
        field.load_backup()

    result = list()

    while len(result) < n:
        assert any(move_count)
        idx = move_count.index(max(move_count))
        move_count[idx] = 0
        if spear_walked[idx] < 2: continue
        if len(paths[idx]) < min_lfp + 4: continue
        if paths[idx] in [paths[r] for r in result]: continue
        result.append(idx)
    return [covers[r] for r in result]


def calc_covered_gen(field):
    df = danger_field.DField(field, max_spear=18, max_answer=5000)
    field.save_backup()
    for c in df:
        map(field.add_spear, c[1])
        yield copy.deepcopy(field)
        field.load_backup()


def calc_covered_one(field, n):
    df = danger_field.DField(field, max_spear=18, max_answer=2000)
    covers = (s[1] for s in df)
    good_covers = choice_good_covers(field, covers, 3)
    field.save_backup()
    result = list()
    for c in good_covers:
        map(field.add_spear, c)
        result.append(copy.deepcopy(field))
        field.load_backup()
    return result


def covered(field, covers):
    field.save_backup()
    for cover in covers:
        map(field.add_spear, cover)
        yield field
        field.load_backup()


def alternative_path_lens(field):
    s = solver.Solver(field)
    s.run()
    return s.alternative_path_lens()