from requests import Response
import json


# ==========================================
# Assertions — статические методы для проверки ответов API.
# Все методы бросают AssertionError с описательным сообщением при провале.
# Используются во всех тестах через Assertions.assert_*().
# ==========================================


class Assertions:
    # Проверить что JSON-ключ существует и его значение равно expected_value
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"
        assert response_as_dict[name] == expected_value, error_message

    # Проверить что JSON-ключ существует в ответе
    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"

    # Проверить HTTP status code
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexp stat code! Exp: {expected_status_code}, Act: {response.status_code}"

    # Проверить что JSON-ключ ОТСУТСТВУЕТ в ответе
    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name not in response_as_dict, f"Response shouldn't have a key {name}, but it has!"

    # Проверить что ВСЕ ключи из списка присутствуют в JSON
    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        for name in names:
            assert name in response_as_dict, f"Response has no key {name}"

    # ==========================================
    # ДОБАВЛЕНО: новые методы-помощники, которых раньше не было
    # ==========================================

    # Проверить что JSON-ключ существует но его значение НЕ равно unexpected_value.
    # Полезно когда API может вернуть разные валидные значения.
    @staticmethod
    def assert_json_value_not_by_name(response: Response, name, unexpected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"
        assert response_as_dict[name] != unexpected_value, error_message

    # Проверить время ответа — падает если ответ дольше max_seconds.
    # response.elapsed — timedelta, измеряется автоматически библиотекой requests.
    @staticmethod
    def assert_response_time(response: Response, max_seconds: float):
        elapsed = response.elapsed.total_seconds()
        assert elapsed <= max_seconds, \
            f"Response too slow! Max: {max_seconds}s, Actual: {elapsed:.3f}s"
