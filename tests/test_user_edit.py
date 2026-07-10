import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# Тесты на изменение данных пользователя: PUT /api/user/{id}
#
# FIX: полностью переписан для добавления:
# 1. _cleanup() + teardown_method — автозатирка созданных тестовых юзеров
#    после каждого теста. Раньше юзеры копились в базе навсегда.
# 2. _register_and_login() — общий метод, убирает дублирование кода.
#    Раньше каждый тест писал register+login вручную (10+ строк копипасты).
# 3. Маркеры @pytest.mark.positive / @pytest.mark.negative для фильтрации.
# ==========================================

url_get = "/api/user/"
url_login = "/api/user/login"


@allure.epic("Тесты на изменение данных пользователя")
class TestUserEdit(BaseCase):
    # Список созданных в этом тесте пользователей для последующей очистки.
    # Классовый атрибут — общий для всех тестов в классе.
    _created_users = []

    # Очистка: залогиниться под каждым созданным юзером и удалить его.
    # Вызывается автоматически после каждого теста через teardown_method.
    # try/except нужен чтобы cleanup не падал если юзер уже удалён
    # или API недоступен — иначе один failed cleanup убьёт все остальные тесты.
    def _cleanup(self):
        for user in self._created_users:
            try:
                resp = MyReq.post(url_login, json={
                    "email": user["email"],
                    "password": user["password"],
                })
                if resp.status_code == 200:
                    token = self.get_header(resp, "x-csrf-token")
                    sid = self.get_cookie(resp, "auth_sid")
                    MyReq.delete(
                        f"/api/user/{user['user_id']}",
                        headers={"x-csrf-token": token},
                        cookies={"auth_sid": sid},
                    )
            except Exception:
                pass
        self._created_users.clear()

    # pytest вызывает teardown_method после каждого теста в классе
    def teardown_method(self):
        self._cleanup()

    # Хелпер: регистрация + логин, возвращает dict с user_id, email, password,
    # token, auth_sid. Юзер автоматически добавляется в _created_users для cleanup.
    def _register_and_login(self):
        data = self.prepare_reg_user_data()
        resp = MyReq.post(url_get, json=data)
        Assertions.assert_code_status(resp, 200)
        uid = self.get_json_value(resp, "id")
        user = {
            "user_id": uid,
            "email": data["email"],
            "password": data["password"],
        }
        self._created_users.append(user)

        login_resp = MyReq.post(url_login, json={
            "email": data["email"],
            "password": data["password"],
        })
        Assertions.assert_code_status(login_resp, 200)
        return {
            **user,
            "token": self.get_header(login_resp, "x-csrf-token"),
            "auth_sid": self.get_cookie(login_resp, "auth_sid"),
        }

    @allure.description("Изменение данных авторизованным пользователем")
    @pytest.mark.positive
    def test_edit_user_authorised(self):
        user = self._register_and_login()

        new_name = "Pupa_lupa"
        response3 = MyReq.put(
            f"/api/user/{user['user_id']}",
            headers={"x-csrf-token": user["token"]},
            cookies={"auth_sid": user["auth_sid"]},
            json={"firstName": new_name},
        )
        Assertions.assert_code_status(response3, 200)

        # GET чтобы убедиться что изменение сохранилось
        response4 = MyReq.get(
            f"/api/user/{user['user_id']}",
            headers={"x-csrf-token": user["token"]},
            cookies={"auth_sid": user["auth_sid"]},
        )
        Assertions.assert_json_value_by_name(
            response4, "firstName", new_name, "Wrong data after edit!"
        )

    @allure.description("Изменение данных неавторизованным пользователем")
    @pytest.mark.negative
    def test_edit_user_unauthorised(self):
        user = self._register_and_login()

        # PUT без headers/cookies — нет авторизации
        new_name = "Umpa_Lumpa"
        response3 = MyReq.put(
            f"/api/user/{user['user_id']}",
            json={"firstName": new_name},
        )
        Assertions.assert_code_status(response3, 400)

    @allure.description("Изменение данных другого пользователя")
    @pytest.mark.negative
    def test_cannot_edit_another_users_data(self):
        # Два разных юзера: A логинится, пытается изменить B
        user_a = self._register_and_login()
        user_b = self._register_and_login()

        new_name = "Pupa_lupa"
        response4 = MyReq.put(
            f"/api/user/{user_b['user_id']}",
            headers={"x-csrf-token": user_a["token"]},
            cookies={"auth_sid": user_a["auth_sid"]},
            json={"firstName": new_name},
        )
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_json_value_by_name(
            response4, "error",
            "This user can only edit their own data.",
            "Expected error message when editing another user's data",
        )

    @allure.description("Изменение данных с невалидными данными")
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "field, invalid_value, expected_error",
        [
            ("email", "invalidemail.com", "Invalid email format"),
            ("firstName", "A", "The value for field `firstName` is too short"),
        ],
        ids=["wrongmail", "oneletterName"],
    )
    def test_edit_user_with_invalid_data(self, field, invalid_value, expected_error):
        user = self._register_and_login()

        response3 = MyReq.put(
            f"/api/user/{user['user_id']}",
            headers={"x-csrf-token": user["token"]},
            cookies={"auth_sid": user["auth_sid"]},
            json={field: invalid_value},
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3, "error", expected_error, "Expected error message"
        )
