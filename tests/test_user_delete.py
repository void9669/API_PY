import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

# ==========================================
# Тесты на удаление пользователя: DELETE /api/user/{id}
#
# FIX: полностью переписан для добавления:
# 1. _cleanup() + teardown_method — автозатирка тестовых юзеров после каждого теста.
# 2. _register_and_login() — убирает дублирование register+login кода.
# 3. В test_user_delete_positive: "if user in self._created_users" перед remove,
#    потому что teardown мог уже очистить список до того как дошли до remove.
# 4. Маркеры positive/negative для фильтрации тестов.
# ==========================================

url_login = "/api/user/login"
url_auth = "/api/user/auth"
url_get = "/api/user/"


@allure.epic("Тесты на удаление данных пользователя")
class TestUserDelete(BaseCase):
    # Список созданных юзеров для cleanup (аналогично test_user_edit.py)
    _created_users = []

    # Cleanup: логинимся под каждым юзером и удаляем его.
    # try/except чтобы один failed cleanup не убил остальные тесты.
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

    def teardown_method(self):
        self._cleanup()

    # Хелпер: регистрация + логин + трекинг для cleanup
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

    # Попытка удалить защищённого тестового юзера (ID 1-5) → 400
    @allure.description("Удаление тестового пользователя запрещено")
    @pytest.mark.negative
    def test_delete_user_id_2(self):
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234",
        }

        response = MyReq.post(url_login, json=login_data)
        Assertions.assert_code_status(response, 200)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # Получаем user_id через auth-эндпоинт
        response1 = MyReq.get(
            url_auth,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        user_id = self.get_json_value(response1, "user_id")
        Assertions.assert_code_status(response1, 200)

        url_delete = f"/api/user/{user_id}"
        response2 = MyReq.delete(
            url_delete,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2, "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Assertion error!",
        )

    # Positive: регистрация → логин → удаление → проверка что юзер исчез
    @allure.description("Регистрация, удаление того-же пользователя")
    @pytest.mark.positive
    def test_user_delete_positive(self):
        user = self._register_and_login()

        url_delete = f"/api/user/{user['user_id']}"
        response3 = MyReq.delete(
            url_delete,
            headers={"x-csrf-token": user["token"]},
            cookies={"auth_sid": user["auth_sid"]},
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3, "success", "!", "Assertion error!"
        )

        # GET после удаления должен вернуть 404
        response4 = MyReq.get(
            f"/api/user/{user['user_id']}",
            headers={"x-csrf-token": user["token"]},
            cookies={"auth_sid": user["auth_sid"]},
        )
        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found"

        # FIX: проверяем "if user in list" перед remove(), потому что
        # teardown_method мог уже вызвать _cleanup() и очистить список
        if user in self._created_users:
            self._created_users.remove(user)

    # Negative: юзер A логинится и пытается удалить юзера B → 400
    @allure.description("Регистрация, удаление другого пользователя")
    @pytest.mark.negative
    def test_cannot_delete_another_users(self):
        user_a = self._register_and_login()
        user_b = self._register_and_login()

        url_delete = f"/api/user/{user_b['user_id']}"
        response3 = MyReq.delete(
            url_delete,
            headers={"x-csrf-token": user_a["token"]},
            cookies={"auth_sid": user_a["auth_sid"]},
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3, "error",
            "This user can only delete their own account.",
            "Assertion error!",
        )
