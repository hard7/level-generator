import scripts


if __name__ == '__main__':
    gen = scripts.load_template_ascii_gen_from_file('mx.tl')
    fields, _ = scripts.init_correct_field_by_ascii_gen(gen)
    scripts.show_path_count_for_fields(fields)





