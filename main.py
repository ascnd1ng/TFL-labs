from lstar import LStar

if __name__ == '__main__':
    table = LStar('NSWE')
    table.generate_graph(2, 1, 1)
    table.extend_table()

    response = table.check_table(table.get_table_json())

    while response != "true":
        table.add_suffixes_from_word(response)
        table.extend_table()
        response = table.check_table(table.get_table_json())
