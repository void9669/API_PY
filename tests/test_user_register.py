import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

url_reg = "https://playground.learnqa.ru/api/user/"

class TestUserRegister(BaseCase):
    def setup(self):
        basepart = "learnqa"
        domain = "example.com"
        randpart = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{basepart}{randpart}@{domain}"

    def test_create_user_happy_path(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post(url_reg, json=data)
        assert response.status_code == 200, f"Unexp stat code {response.status_code}"
        Assertions.assert_json_has_key(response, "id")


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
        response = requests.post(url_reg, json=data)
        assert response.status_code == 400, f"Unexp st code {response.status_code}"
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}"