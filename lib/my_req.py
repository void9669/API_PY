import requests
from lib.logger import Logger
import allure
from environment import ENV_OBJECT

# ==========================================
# FIX: добавлен DEFAULT_TIMEOUT — по умолчанию 10 секунд на каждый запрос.
# Раньше timeout не задавался, и тест мог зависнуть навечно если API не отвечает.
# Теперь каждый метод (get/post/put/delete/patch) принимает необязательный
# параметр timeout и пробрасывает его в requests.<method>(timeout=...).
# ==========================================
DEFAULT_TIMEOUT = 10


# ==========================================
# MyReq — обёртка над requests для централизованных HTTP-запросов.
# Все запросы проходят через _send(), который:
#   1. Добавляет base URL из ENV_OBJECT
#   2. Логирует запрос и ответ через Logger
#   3. Пакует each запрос в Allure step для отчёта
# ==========================================
class MyReq():
    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None, cookies: dict = None, timeout: int = DEFAULT_TIMEOUT):
        with allure.step(f"GET req to '{url}'"):
            return MyReq._send(url, params, headers, cookies, "GET", timeout)

    @staticmethod
    def post(url: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = DEFAULT_TIMEOUT):
        with allure.step(f"POST req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, "POST", timeout)

    @staticmethod
    def put(url: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = DEFAULT_TIMEOUT):
        with allure.step(f"PUT req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, "PUT", timeout)

    @staticmethod
    def delete(url: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = DEFAULT_TIMEOUT):
        with allure.step(f"DELETE req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, "DELETE", timeout)

    # FIX: добавлен PATCH — раньше этого метода не было, а API может его требовать
    @staticmethod
    def patch(url: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = DEFAULT_TIMEOUT):
        with allure.step(f"PATCH req to '{url}'"):
            return MyReq._send(url, json, headers, cookies, "PATCH", timeout)

    # Внутренний метод: склеивает base_url, логирует, делает запрос, логирует ответ.
    # data передаётся как params для GET и как json для POST/PUT/DELETE/PATCH.
    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str, timeout: int):
        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_req(url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(url, params=data, headers=headers, cookies=cookies, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, cookies=cookies, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, cookies=cookies, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, json=data, headers=headers, cookies=cookies, timeout=timeout)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers, cookies=cookies, timeout=timeout)
        else:
            raise Exception(f"Bad method '{method}'")

        Logger.add_resp(response)

        return response