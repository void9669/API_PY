from json.decoder import JSONDecodeError
import requests

payload = {"name" : "User"}
response =requests.get("https://playground.learnqa.ru/api/get_text", params = payload)
print(response.text)

try:
    parsed_txt = response.json()
    print(parsed_txt)
except JSONDecodeError:
    print("Response isn't JSON")