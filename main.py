import time

from lstar import LStar


def measure_time(func):
    def wrapper():
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"Время выполнения {func.__name__}: {end_time - start_time:.4f} секунд")
        return result

    return wrapper


@measure_time
def main():
    table = LStar('NSWE')
    print('Введите n:')
    n = int(input())
    print('Введите m:')
    m = int(input())
    print('Введите число выходов:')
    exit_num = int(input())

    table.generate_graph(n, m, exit_num)

    table.extend_table()
    response = table.check_table(table.get_table_json())
    print(f'Контрпример: {response}')

    while True:
        table.add_suffixes_from_counter_example(response)
        table.extend_table()
        response = table.check_table(table.get_table_json())
        if response != "true":
            print(f'Контрпример: {response}')
        else:
            break

    print(table)


main()
