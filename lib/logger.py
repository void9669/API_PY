import datetime
import os
from requests import Response

class Logger:
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_log(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_req(cls, url:str, data:dict, headers:dict, cookies:dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Method: {method}\n"
        data_to_add += f"URL: {url}\n"
        data_to_add += f"data: {data}\n"
        data_to_add += f"headers:  {headers}\n"
        data_to_add += f"cookies: {cookies}\n"
        data_to_add += "\n"

    cls._write_log(data_to_add)

    @classmethod
    def add_resp(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n" 
        data_to_add = f"\n-----\n"

        cls._write_log(data_to_add)


