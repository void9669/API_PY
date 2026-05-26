import json.decoder
from datetime import datetime

from requests import Response

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't find cookie {cookie_name}"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't find header {headers_name}"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"

        return response_as_dict[name]

    def prepare_reg_user_data(self, email=None):
        if email is None:
            basepart = "learnqa"
            domain = "example.com"
            randpart = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{basepart}{randpart}@{domain}"
        return {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }     