import json

from tabulate import tabulate

from session import Session


class LStar(Session):
    def __init__(self, alphabet_str):
        super().__init__()
        self.main_table = {"": ['0']}
        self.complementary_table = {}
        self.suffixes = [""]
        self.alphabet = list(alphabet_str)
        self.epsilon = 'e'

    def build_main_prefixes(self):
        for complementary_prefix, row in list(self.complementary_table.items()):
            if row not in list(self.main_table.values()):
                self.main_table[complementary_prefix] = row
                self.complementary_table.pop(complementary_prefix)

    def add_prefix(self, prefix):
        if prefix in self.complementary_table or prefix in self.main_table:
            return
        self.complementary_table[prefix] = []
        for suffix in self.suffixes:
            self.complementary_table[prefix].append(self.check_membership(
                prefix + suffix))

    def extend_table(self):
        for main_prefix in self.main_table:
            for letter in self.alphabet:
                self.add_prefix(main_prefix + letter)
        self.build_main_prefixes()

    def add_suffixes_from_counter_example(self, counter_example):
        for i in range(len(counter_example)):
            suffix = counter_example[-i:]
            if suffix not in self.suffixes:
                self.suffixes.append(suffix)

                for main_prefix in self.main_table:
                    response = self.check_membership(main_prefix + suffix)
                    self.main_table[main_prefix].append(response)

                for complementary_prefix in self.complementary_table:
                    response = self.check_membership(complementary_prefix + suffix)
                    self.complementary_table[complementary_prefix].append(response)
        self.build_main_prefixes()

    def replace_empty_with_epsilon(self, lst):
        return [self.epsilon if x == '' else x for x in lst]

    def get_table_json(self):
        main_prefixes = []
        complementary_prefixes = []
        suffixes = []
        table = []
        for main_prefix in self.main_table:
            main_prefixes.append(main_prefix)

        for complementary_prefix in self.complementary_table:
            complementary_prefixes.append(complementary_prefix)

        for suffix in self.suffixes:
            suffixes.append(suffix)

        for main_prefix in main_prefixes:
            for i in range(len(suffixes)):
                table.append(str(self.main_table[main_prefix][i]))

        for complimentary_prefix in complementary_prefixes:
            for i in range(len(suffixes)):
                table.append(str(self.complementary_table[complimentary_prefix][i]))

        main_prefixes = self.replace_empty_with_epsilon(main_prefixes)
        suffixes = self.replace_empty_with_epsilon(suffixes)
        main_prefixes_str = " ".join(main_prefixes)
        complementary_prefixes_str = " ".join(complementary_prefixes)
        suffixes_str = " ".join(suffixes)
        table_str = "".join(table)

        return [main_prefixes_str,
                complementary_prefixes_str,
                suffixes_str,
                table_str]

    def __str__(self):
        output_table = [[""] + self.suffixes]  # Заголовок с пустой ячейкой слева и суффиксами сверху

        # Добавляем строки с содержимым `main_table`
        for key in self.main_table:
            row = [key] + self.main_table[key]
            output_table.append(row)

        # Добавляем строку с разделителем "+"
        output_table.append(["+"] + [""] * (len(self.suffixes) - 1))

        # Добавляем строки с содержимым `extended_table`
        for key in self.complementary_table:
            row = [key] + self.complementary_table[key]
            output_table.append(row)

        # Форматируем таблицу с помощью `tabulate`
        return tabulate(output_table, headers="firstrow", tablefmt="github")
