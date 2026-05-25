from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"

        assert name in response_as_dict, f"Response has no key {name}"
        assert response_as_dict[name] == expected_value, error_message
    
    @staticmethod    
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"
            
        assert name in response_as_dict, f"Response has no key {name}"

    @staticmethod    
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexp stat code! Exp: {expected_status_code}, Act: {response.status_code}"

    @staticmethod    
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response isn't JSON, it's {response.text}"
            
        assert name not in response_as_dict, f"Response shouldn't have a key {name}, but it has!"