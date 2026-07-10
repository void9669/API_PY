import json.decoder
import uuid  # FIX: заменён datetime на uuid — генерация уникальных email без коллизий при параллельных тестах

from requests import Response


# ==========================================
# BaseCase — базовый класс для всех тестов.
# Содержит вспомогательные методы для извлечения данных из ответа.
# Все тестовые классы наследуют его и получают эти методы через self.
# ==========================================


class BaseCase:
    # Извлечь cookie по имени; AssertionError если cookie нет в ответе
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't find cookie {cookie_name}"
        return response.cookies[cookie_name]

    # Извлечь header по имени; AssertionError если header нет в ответе
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't find header {headers_name}"
        return response.headers[headers_name]

    # Извлечь значение из JSON-ответа по ключу; падает если нет JSON или ключа
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"

        return response_as_dict[name]

    # Генерация данных для регистрации пользователя.
    # FIX: ранее использовалась datetime.now().strftime() — при параллельных
    # тестах в одну секунду email-ы совпадали, что вызывало 400 "already exists".
    # uuid.uuid4().hex[:8] — уникальный случайный суффикс, коллизий практически нет.
    def prepare_reg_user_data(self, email=None):
        if email is None:
            basepart = "learnqa"
            domain = "example.com"
            randpart = uuid.uuid4().hex[:8]
            email = f"{basepart}{randpart}@{domain}"
        return {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }     