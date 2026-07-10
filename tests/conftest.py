import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# conftest.py — файл конфигурации pytest.
# Автоматически подхватывается pytest, fixtures здесь доступны
# во ВСЕХ тестах в директории tests/ без явного импорта.
#
# FIX: ранее код register+login дублировался в каждом тестовом классе
# отдельным методом _register_and_login(). Теперь общая логика в fixtures.
# ==========================================

base_case = BaseCase()


@pytest.fixture(scope="function")
def register_and_login():
    """Зарегистрировать нового пользователя, залогиниться, вернуть данные с auth.

    Возвращает dict:
        user_id, email, password, auth_sid, token

    Использование в тесте:
        def test_something(self, register_and_login):
            user = register_and_login
            ... user["auth_sid"], user["token"] ...
    """
    data = base_case.prepare_reg_user_data()
    response = MyReq.post("/api/user/", json=data)
    Assertions.assert_code_status(response, 200)
    Assertions.assert_json_has_key(response, "id")

    user_id = base_case.get_json_value(response, "id")
    email = data["email"]
    password = data["password"]

    login_response = MyReq.post("/api/user/login", json={
        "email": email,
        "password": password,
    })
    Assertions.assert_code_status(login_response, 200)

    auth_sid = base_case.get_cookie(login_response, "auth_sid")
    token = base_case.get_header(login_response, "x-csrf-token")

    return {
        "user_id": user_id,
        "email": email,
        "password": password,
        "auth_sid": auth_sid,
        "token": token,
    }


@pytest.fixture(scope="function")
def two_users():
    """Зарегистрировать двух пользователей и залогинить обоих.

    Возвращает dict {"a": {...}, "b": {...}} с auth-данными каждого.
    Полезно для тестов где один юзер пытается изменить/удалить другого.

    __wrapped__() вызывает функцию напрямую (без fixture-обёртки),
    чтобы получить dict вместо fixture-значения pytest.
    """
    user_a = register_and_login.__wrapped__()
    user_b = register_and_login.__wrapped__()
    return {"a": user_a, "b": user_b}
