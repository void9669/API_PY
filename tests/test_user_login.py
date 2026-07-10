import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# Тесты на эндпоинт логина: POST /api/user/login
#
# ДОБАВЛЕНО: этот файл целиком новый.
# Раньше не было ни одного теста на login — только register, edit, delete, get.
# Login — критический путь, без которого невозможны edit/delete
# (нужен token + auth_sid для авторизации).
#
# Тесты покрывают:
# - Happy path (регистрация + логин)
# - Wrong password
# - Nonexistent email
# - Empty email / password
# - Missing fields
#
# Примечание: API возвращает plain text ошибки (не JSON),
# поэтому проверки идут через response.text, а не assert_json_value_by_name.
# ==========================================

url_login = "/api/user/login"
url_reg = "/api/user/"


@allure.epic("Login Cases")
class TestUserLogin(BaseCase):

    # Логин с правильным email, но неверным паролем → 400
    @allure.description("Login with wrong password")
    @pytest.mark.negative
    def test_login_wrong_password(self):
        # Сначала регистрируем пользователя чтобы email существовал в базе
        data = self.prepare_reg_user_data()
        reg_response = MyReq.post(url_reg, json=data)
        Assertions.assert_code_status(reg_response, 200)

        # Пробуем залогиниться с неправильным паролем
        login_response = MyReq.post(url_login, json={
            "email": data["email"],
            "password": "wrong_password_999",
        })
        Assertions.assert_code_status(login_response, 400)
        # API возвращает plain text, не JSON → проверяем через .text
        assert login_response.text == "Invalid username/password supplied", \
            f"Unexpected error: {login_response.text}"

    # Логин с несуществующим email → 400
    @allure.description("Login with nonexistent email")
    @pytest.mark.negative
    def test_login_nonexistent_email(self):
        login_response = MyReq.post(url_login, json={
            "email": "nonexistent_user_xyz@example.com",
            "password": "123",
        })
        Assertions.assert_code_status(login_response, 400)
        assert login_response.text == "Invalid username/password supplied", \
            f"Unexpected error: {login_response.text}"

    # Логин с пустым email → 400
    @allure.description("Login with empty email")
    @pytest.mark.negative
    def test_login_empty_email(self):
        login_response = MyReq.post(url_login, json={
            "email": "",
            "password": "123",
        })
        Assertions.assert_code_status(login_response, 400)

    # Логин с пустым паролем → 400
    @allure.description("Login with empty password")
    @pytest.mark.negative
    def test_login_empty_password(self):
        login_response = MyReq.post(url_login, json={
            "email": "vinkotov@example.com",
            "password": "",
        })
        Assertions.assert_code_status(login_response, 400)

    # Логин без поля email в body → 400
    @allure.description("Login with missing email field")
    @pytest.mark.negative
    def test_login_missing_email_field(self):
        login_response = MyReq.post(url_login, json={
            "password": "123",
        })
        Assertions.assert_code_status(login_response, 400)

    # Логин без поля password в body → 400
    @allure.description("Login with missing password field")
    @pytest.mark.negative
    def test_login_missing_password_field(self):
        login_response = MyReq.post(url_login, json={
            "email": "vinkotov@example.com",
        })
        Assertions.assert_code_status(login_response, 400)

    # Happy path: регистрация → логин → проверяем что получили token и cookie
    @allure.description("Happy path login")
    @pytest.mark.positive
    def test_login_happy_path(self):
        data = self.prepare_reg_user_data()
        reg_response = MyReq.post(url_reg, json=data)
        Assertions.assert_code_status(reg_response, 200)

        login_response = MyReq.post(url_login, json={
            "email": data["email"],
            "password": data["password"],
        })
        Assertions.assert_code_status(login_response, 200)
        Assertions.assert_json_has_key(login_response, "user_id")
        # Проверяем что авторизация выдала нужные credentials для后续 запросов
        self.get_cookie(login_response, "auth_sid")
        self.get_header(login_response, "x-csrf-token")
