import time

from lstar import LStar

if __name__ == '__main__':
    start_time = time.time()

    table = LStar('NSWE')
    table.generate_graph(6, 5, 3)
    table.extend_table()
    table.build_main_prefixes()

    response = table.check_table(table.get_table_json())

    while response != "true":
        table.add_suffixes_from_word(response)
        table.build_main_prefixes()
        table.extend_table()
        table.build_main_prefixes()
        response = table.check_table(table.get_table_json())
        if response != "true":
            print(f'Новый контрпример: {response}')

    print(table)
    finish_time = time.time()
    print(f'Успешно решено за {finish_time - start_time}')


