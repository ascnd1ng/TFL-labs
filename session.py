import json

import requests


class Session:
    def __init__(self):
        self.session = requests.Session()
        self.check_membership_counter = 0
        self.check_table_counter = 0

    def check_membership(self, word):
        self.check_membership_counter += 1

        url = "http://127.0.0.1:8080/check_membership"
        try:
            response = self.session.post(
                url,
                headers={"Content-Type": "application/json"},
                data=word
            )

            return response.text
        except requests.exceptions.RequestException as e:
            print(f"check_membership: ({word}): {e}")
            return None

    def check_table(self, args):
        self.check_table_counter += 1

        data = {
            "main_prefixes": args[0],
            "complementary_prefixes": args[1],
            "suffixes": args[2],
            "table": args[3]
        }
        url = "http://127.0.0.1:8080/check_table"

        try:
            response = self.session.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data))

            if response.status_code == 200:
                answer = response.text
                return answer

        except requests.RequestException as e:
            print(f"check_table: {e}")
            return None

    def generate_graph(self, n, m, exit_num, wall_break):
        url = "http://127.0.0.1:8080/generate_graph"
        data = {
            "num_of_finish_edge": exit_num,  # количество конечных рёбер
            "pr_of_break_wall": wall_break,  # вероятность "разрыва стены"
            "width": m,  # ширина графа
            "height": n  # высота графа
        }

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)
            )

            if response.status_code == 200:
                print("Граф успешно сгенерирован")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
