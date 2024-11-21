import json
from itertools import groupby

from tabulate import tabulate

from session import Session


class LStar(Session):
    def __init__(self, alphabet_str, n, m):
        super().__init__()
        self.main_table = {"": ['0']}
        self.complementary_table = {}
        self.suffixes = [""]
        self.alphabet = list(alphabet_str)
        self.epsilon = 'e'
        self.n = n
        self.m = m

    def opt1(self, prefix):
        # 2n + 3 x 2m + 3
        serie = 0
        letter = '#'
        new_prefix = list()
        for current_letter in prefix:
            if current_letter != letter:
                serie = 1
                letter = current_letter
                new_prefix.append(current_letter)
            else:
                serie += 1
                if letter == 'N' or letter == 'S' and serie <= self.n * 2 + 2:
                    new_prefix.append(current_letter)
                if letter == 'W' or letter == 'E' and serie <= self.m * 2 + 2:
                    new_prefix.append(current_letter)
        return ''.join(new_prefix)

    def apply_simplify_rule(self, block, a, b):
        block = ''.join(block)
        grouped_letters = [[char, len(list(group))] for char, group in groupby(block)]
        group_len = len(grouped_letters)

        grouped_letters.append([a, 0])
        i = 1
        while i < group_len:
            if grouped_letters[i][0] == b:
                z = grouped_letters[i + 1][1]
                y = grouped_letters[i][1]
                x = grouped_letters[i - 1][1]

                if y <= x and z >= y:
                    grouped_letters[i + 1][1] = x + z - y
                    grouped_letters[i][1] = 0
                    grouped_letters[i - 1][1] = 0
            i += 1
        result = ''.join(group[0] * group[1] for group in grouped_letters)
        return result

    def shorten_block(self, block):
        if block[0] == 'N' or block[0] == 'S':
            block = self.apply_simplify_rule(block, 'N', 'S')
            block = self.apply_simplify_rule(block, 'S', 'N')
        else:
            block = self.apply_simplify_rule(block, 'W', 'E')
            block = self.apply_simplify_rule(block, 'E', 'W')
        return block
    def opt2(self, prefix):
        type_by_letter = {'N': 'vertical', 'S': 'vertical', 'W': 'horizontal', 'E': 'horizontal'}
        blocks = [[prefix[0]]]

        for i in range(1, len(prefix)):
            current_letter = prefix[i]
            if type_by_letter[blocks[-1][0]] == type_by_letter[current_letter]:
                blocks[-1].append(current_letter)
            else:
                blocks.append([current_letter])

        for block in blocks:
            block = self.shorten_block(block)
        result = ''.join(''.join(block) for block in blocks)

        return result

    def build_main_prefixes(self):
        for complementary_prefix, row in list(self.complementary_table.items()):
            if row not in list(self.main_table.values()):
                self.main_table[complementary_prefix] = row
                self.complementary_table.pop(complementary_prefix)

    def add_prefix(self, prefix):
        prefix = self.opt1(prefix)
        prefix = self.opt2(prefix)
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
            suffix = counter_example[-1 - i:]
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
        table_rows = [["Main prefixes / Suffixes"] + self.replace_empty_with_epsilon(self.suffixes)]

        for main_prefix in self.main_table:
            row = [main_prefix] + self.main_table[main_prefix]
            if main_prefix == '':
                row[0] = self.epsilon
            table_rows.append(row)

        table_rows.append(["Complementary prefixes"] + ["*"] * (len(self.suffixes) - 1))

        for complementary_prefix in self.complementary_table:
            row = [complementary_prefix] + self.replace_empty_with_epsilon(self.complementary_table[complementary_prefix])

            table_rows.append(row)

        return tabulate(table_rows, headers="firstrow", tablefmt="fancy_grid")
