import requests
from lib.loggger import Logger

class MyReq():
    @staticmethod
    def get (url:str, data:dict=None, headers:dict=None, cookies:dict=None ):
        return MyReq._send(url, data, headers, cookies, 'GET')
    
    def post (url:str, data:dict=None, headers:dict=None, cookies:dict=None ):
        return MyReq._send(url, data, headers, cookies, 'POST')
    
    def put (url:str, data:dict=None, headers:dict=None, cookies:dict=None ):
        return MyReq._send(url, data, headers, cookies, 'PUT')
    
    def delete (url:str, data:dict=None, headers:dict=None, cookies:dict=None ):
        return MyReq._send(url, data, headers, cookies, 'DELETE')

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