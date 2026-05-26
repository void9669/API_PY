import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

url_get = "https://playground.learnqa.ru/api/user/"
url_login = "https://playground.learnqa.ru/api/user/login"

class TestUserEdit(BaseCase):
    def test_edit_user(self):

        #register
        register_data = self.prepare_reg_user_data()
        response1 = requests.post(url_get, json=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #login
        login_data = {
            'email' : email,
            'password' : password
        }

        response2 = requests.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #edit
        new_name = "Pupa_lupa"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid},
            json={"firstName":new_name})

        Assertions.assert_code_status(response3, 200)

        #get
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid}
        )   

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong data after edit! Current {new_name}"
        )










