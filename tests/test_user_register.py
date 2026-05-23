import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

url_reg = "https://playground.learnqa.ru/api/user/"

class TestUserRegister(BaseCase):
    def test_create_user_with_ex_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
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
        response = requests.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
        assert response.content.decode("utf-8") == f"Invalid email format"
    
    @pytest.mark.parametrize('missing_field', [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ],
    ids =["nopass", "nousername", "nofirst", "nolast", "noemail"]
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
        response = requests.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}"