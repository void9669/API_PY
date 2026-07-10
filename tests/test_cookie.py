import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# FIX: этот файл был создан заново (старый test_cookie.py в корне удалён).
#
# Проблемы старой версии:
# 1. MyReq использовался без импорта — файл падал при запуске
# 2. Файл лежал в корне проекта, а не в tests/ — pytest его не находил
# 3. Строки на уровне модуля (вне функций) вызывали HTTP-запросы
#    при import-time, во время сбора тестов
#
# Теперь: файл в tests/, правильные импорты, чистый pytest-class стиль.
# ==========================================

url_cookie = "/api/homework_cookie"


@allure.epic("Cookie and Header Homework Cases")
class TestCookie(BaseCase):

    @allure.description("Проверка значения cookie HomeWork")
    def test_cookie_value(self):
        response = MyReq.get(url_cookie)

        Assertions.assert_code_status(response, 200)

        # Получаем cookie по имени и проверяем значение.
        # API возвращает plain text, поэтому JSON-проверки не нужны —
        # просто берём cookie из ответа напрямую.
        cookie_value = self.get_cookie(response, "HomeWork")
        assert cookie_value == "hw_value", \
            f"Expected cookie value 'hw_value', got '{cookie_value}'"
