import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_req import MyReq

url_get = "/api/user/"
url_login = "/api/user/login"

@allure.epic("Тесты на изменение данных пользователя")
class TestUserEdit(BaseCase):

    @allure.description("Изменение данных авторизованным пользователем")
    def test_edit_user_authorised(self):

        #register
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

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

        response2 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #edit
        new_name = "Pupa_lupa"

        response3 = MyReq.put(
            f"/api/user/{user_id}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid},
            json={"firstName":new_name})

        Assertions.assert_code_status(response3, 200)

        #get
        response4 = MyReq.get(
            f"/api/user/{user_id}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid}
        )   

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong data after edit!"
        )
    
    @allure.description("Изменение данных неавторизованным пользователем")    
    def test_edit_user_unauthorised(self):

        #register
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

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

        response2 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #edit
        new_name = "Umpa_Lumpa"

        response3 = MyReq.put(
            f"/api/user/{user_id}",
            json={"firstName":new_name})

        Assertions.assert_code_status(response3, 400)

    @allure.description("Изменение данных другого пользователя")
    def test_cannot_edit_another_users_data(self):

        #register1
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #register2
        register_data = self.prepare_reg_user_data()
        response2 = MyReq.post(url_get, json=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data['email']
        firstName2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response2, "id")

        #login
        login_data = {
            'email' : email,
            'password' : password
        }

        response3 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response3, 200)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        #edit
        new_name = "Pupa_lupa"

        response4 = MyReq.put(
            f"/api/user/{user_id2}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid},
            json={"firstName":new_name})
        
        Assertions.assert_code_status(response4, 400) 
        
        Assertions.assert_json_value_by_name(
            response4,
            "error",
            "This user can only edit their own data.",
            "Expected error message when editing another user's data"
        )

    @allure.description("Изменение данных с невалидными данными")
    @pytest.mark.parametrize(
        "field, invalid_value, expected_error", 
    [
    ("email", "invalidemail.com", "Invalid email format"),
    ("firstName", "A", "The value for field `firstName` is too short")
    ],
    ids =['wrongmail', 'oneletterName'] 
    )
    def test_edit_user_with_invalid_data(self, field, invalid_value, expected_error):
        
        #register
        register_data = self.prepare_reg_user_data()
        response1 = MyReq.post(url_get, json=register_data)

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

        response2 = MyReq.post(url_login, json=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #edit
        response3 = MyReq.put(
            f"/api/user/{user_id}", 
            headers={"x-csrf-token" : token}, 
            cookies={"auth_sid":auth_sid},
            json={field: invalid_value})

        Assertions.assert_code_status(response3, 400)
        
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            expected_error,
            "Expected error message"
        )

    











