import json
from session import Session


class LStar(Session):
    def __init__(self, letters):
        super().__init__()
        self.alphabet = list(letters)
        self.suffixes = [""]
        self.main_table = {"": [0]}
        self.extended_table = {}

    def add_suffixes_from_word(self, word):
        for i in range(len(word) - 1, -1, -1):
            suffix = word[i:]
            if suffix not in self.suffixes:
                self.suffixes.append(suffix)

                for key in self.main_table:
                    response = self.check_membership(key + suffix)
                    self.main_table[key].append(response)

                for key in self.extended_table:
                    response = self.check_membership(key + suffix)
                    self.extended_table[key].append(response)

    def add_prefix(self, prefix):
        self.extended_table[prefix] = []

        for suffix in self.suffixes:
            self.extended_table[prefix].append(self.check_membership(
                prefix + suffix))

    def extend_table(self):
        for main_prefix in self.main_table:
            for letter in self.alphabet:
                self.add_prefix(main_prefix + letter)
        self.build_main_prefixes()

    def build_main_prefixes(self):
        for key, value in list(self.extended_table.items()):
            if value not in self.main_table.values() and list(self.extended_table.values()).count(value) == 1:
                self.main_table[key] = value
                self.extended_table.pop(key)

    def replace_empty_with_e(self, lst):
        return ['e' if x == '' else x for x in lst]

    def get_table_json(self):
        main_prefixes = []
        complementary_prefixes = []
        suffixes = []
        table = []
        for main_prefix in self.main_table:
            main_prefixes.append(main_prefix)

        for complementary_prefix in self.extended_table:
            complementary_prefixes.append(complementary_prefix)

        for suffix in self.suffixes:
            suffixes.append(suffix)

        for main_prefix in main_prefixes:
            for i in range(len(suffixes)):
                table.append(str(self.main_table[main_prefix][i]))

        for complimentary_prefix in complementary_prefixes:
            for i in range(len(suffixes)):
                table.append(str(self.extended_table[complimentary_prefix][i]))

        main_prefixes = self.replace_empty_with_e(main_prefixes)
        suffixes = self.replace_empty_with_e(suffixes)
        main_prefixes_str = " ".join(main_prefixes)
        complementary_prefixes_str = " ".join(complementary_prefixes)
        suffixes_str = " ".join(suffixes)
        table_str = "".join(table)

        return [main_prefixes_str,
                complementary_prefixes_str,
                suffixes_str,
                table_str]
