import datetime
import os
from requests import Response


# ==========================================
# FIX: в add_resp() на старой строке 38 было:
#   data_to_add = f"\n-----\n"
# Это ПОЛНОСТЬЮ СТИРАЛО все данные ответа (status, text, headers, cookies)
# и в лог писал только разделитель "-----".
# Заменено на += чтобы данные ответа ДОБАВЛЯЛИСЬ, а не перезаписывались.
# ==========================================


class Logger:
    # Имя файла лога формируется один раз при импорте модуля.
    # Все запуски пишут в один файл в пределах одного процесса.
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_log(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    # Логирование запроса: сохраняет method, url, data, headers, cookies
    @classmethod
    def add_req(cls, url:str, data:dict, headers:dict, cookies:dict, method: str):
        # PYTEST_CURRENT_TEST — переменная окружения, которую pytest
        # автоматически ставит на имя текущего теста во время выполнения
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

    # Логирование ответа: сохраняет status code, text, headers, cookies
    # FIX: было "=" вместо "+=" — данные ответа терялись
    @classmethod
    def add_resp(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        # FIX: было "=" — перезаписывало всё выше. Теперь "+=" добавляет разделитель
        data_to_add += f"\n-----\n"

        cls._write_log(data_to_add)
