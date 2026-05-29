import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

url_reg = "/api/user/"

class TestUserRegister(BaseCase):

    def test_create_user_happy_path(self):
        data = self.prepare_reg_user_data()

        response = MyReq.post(url_reg, json=data)
        
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_ex_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_reg_user_data(email)

        response = MyReq.post(url_reg, json=data)
        
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexp content {response.content}"
    
    def test_create_user_with_invalid_email(self):
        email = 'vinkotov.example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = MyReq.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
        assert response.content.decode("utf-8") == f"Invalid email format"
    
    @pytest.mark.parametrize('missing_field', [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ],
    ids =["no_pass", "no_username", "no_first", "no_last", "no_email"]
    )

    def test_create_user_missing_field(self, missing_field):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'ass@example.com'
        }
        del data[missing_field]
        response = MyReq.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}"