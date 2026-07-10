import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# FIX: этот файл был создан заново (старый test_headers.py в корне удалён).
#
# Проблемы старой версии:
# 1. MyReq использовался без импорта — файл падал
# 2. response = MyReq.get(url) + print() на уровне модуля —
#    HTTP-запрос выполнялся при import-time (при сборе тестов),
#    а не при реальном запуске теста
# 3. Файл лежал в корне, pytest не мог его найти
#
# Теперь: файл в tests/, чистый pytest-class, запрос только внутри теста.
# ==========================================

url_header = "/api/homework_header"


@allure.epic("Cookie and Header Homework Cases")
class TestHeader(BaseCase):

    @allure.description("Проверка значения заголовка x-secret-homework-header")
    def test_header_value(self):
        response = MyReq.get(url_header)

        Assertions.assert_code_status(response, 200)

        # Получаем custom header по имени и проверяем значение.
        # API возвращает plain text, поэтому JSON-проверки не нужны.
        header_value = self.get_header(response, "x-secret-homework-header")
        assert header_value == "Some secret value", \
            f"Expected header 'Some secret value', got '{header_value}'"
