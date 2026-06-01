import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq
import allure

url_login = "/api/user/login"
url_auth = "/api/user/auth"
url_get = "/api/user/"

@allure.epic("Тесты на удаление данных пользователя")
class TestUserDelete(BaseCase):

    @allure.description("Удаление конкретного пользователя")
    def test_delete_user_id_2(self):
        #login
        login_data = {
            'email' : 'vinkotov@example.com',
            'password' : '1234'
        }

        response = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response, 200)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        
        #deleting
        response1 = MyReq.get(url_auth, 
        headers={"x-csrf-token" : token}, 
        cookies={"auth_sid":auth_sid}
        )
        user_id = self.get_json_value(response1,"user_id")
        Assertions.assert_code_status(response1, 200)

        url_delete = f"/api/user/{user_id}"

        response2 = MyReq.delete(url_delete,
        headers={"x-csrf-token" : token}, 
        cookies={"auth_sid":auth_sid}
        )
        
        print(response2.text, response2.status_code)

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Assertion error!"
        )

    @allure.description("Регистрация, удаление того-же пользователя")
    def test_user_delete_positive(self):

        #register
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id1 = self.get_json_value(response1, "id")

        #login
        login_data = {
            'email' : email,
            'password' : password
        }

        response2 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #deleting
        url_delete = f"/api/user/{user_id1}"

        response3 = MyReq.delete(url_delete,
        headers={"x-csrf-token" : token}, 
        cookies={"auth_sid":auth_sid}
        )
        
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "success",
            "!",
            "Assertion error!"
        )

        #check_id
        response4 = MyReq.get(f"/api/user/{user_id1}",
        headers={"x-csrf-token" : token}, 
        cookies={"auth_sid":auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found"
    
    @allure.description("Регистрация, удаление другого пользователя")
    def test_cannot_delete_another_users(self):

        #register
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id2 = self.get_json_value(response1, "id")

        #login
        login_data = {
            'email' : email,
            'password' : password
        }

        response2 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #register_another_user
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id3 = self.get_json_value(response1, "id")
        
        #deleting
        url_delete = f"/api/user/{user_id3}"

        response3 = MyReq.delete(url_delete,
        headers={"x-csrf-token" : token}, 
        cookies={"auth_sid":auth_sid}
        )
        
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "This user can only delete their own account.",
            "Assertion error!"
        )



        


