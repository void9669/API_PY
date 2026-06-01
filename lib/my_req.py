import requests
from lib.logger import Logger
import allure 

class MyReq():
    @staticmethod
    def get (url:str, params:dict=None, headers:dict=None, cookies:dict=None ):
        with allure.step(f"GET req to '{url}'"):
            return MyReq._send(url, params, headers, cookies, 'GET')
    @staticmethod
    def post (url:str, json:dict=None, headers:dict=None, cookies:dict=None ):
        with allure.step(f"POST req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, 'POST')
    @staticmethod
    def put (url:str, json:dict=None, headers:dict=None, cookies:dict=None ):
        with allure.step(f"PUT req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, 'PUT')
    @staticmethod
    def delete (url:str, json:dict=None, headers:dict=None, cookies:dict=None ):
        with allure.step(f"DELETE req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url:str, data:dict, headers:dict, cookies:dict, method: str ):

        url = f"https://playground.learnqa.ru{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_req(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad method '{method}'")

        Logger.add_resp(response)

        return response