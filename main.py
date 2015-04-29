import scripts


if __name__ == '__main__':
    ascii_gen = scripts.take_template_ascii_from_file('mx.tl')
    f = scripts.init_template_field_by_ascii(ascii_gen.next())
    # scripts.fields2out((f,), '../', 'lev')





