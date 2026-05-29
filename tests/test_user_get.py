import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

url_get = "/api/user/2"
url_login = "/api/user/login"

class TestUserGet(BaseCase):
    def test_get_user_nauth(self):
        response = MyReq.get(url_get)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email" )
        Assertions.assert_json_has_no_key(response, "firstName" )
        Assertions.assert_json_has_no_key(response, "lastName" )

    def test_get_user_auth_same_user(self):
        data = {
            'email':'vinkotov@example.com',
            'password': '1234'
        }
        
        response1 = MyReq.post(url_login, json=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token" )
        user_id_auth = self.get_json_value(response1, "user_id")

        response2 = MyReq.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}", 
        headers = {"x-csrf-token" : token}, 
        cookies = {"auth_sid" : auth_sid}
        )
        exp_fields = ["username","email","firstName", "lastName" ]
        Assertions.assert_json_has_keys(response2, exp_fields)

    def test_get_user_auth_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyReq.post(url_login, json=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyReq.get(
            "https://playground.learnqa.ru/api/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_key(response2, "email")
        Assertions.assert_json_has_no_key(response2, "firstName")
        Assertions.assert_json_has_no_key(response2, "lastName")

