import time

from lstar import LStar

if __name__ == '__main__':
    start_time = time.time()

    table = LStar('NSWE')
    table.generate_graph(4, 5, 2)
    table.extend_table()
    response = table.check_table(table.get_table_json())

    while response != "true":
        table.add_suffixes_from_counter_example(response)
        table.extend_table()
        response = table.check_table(table.get_table_json())
        if response != "true":
            print(f'Новый контрпример: {response}')

    print(table)
    finish_time = time.time()
    print(f'Успешно решено за {finish_time - start_time}')


