import requests
import time


URL = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(URL)
response1 = response.json()
token = response1["token"]
seconds = response1["seconds"]

response2 = requests.get(URL, params={"token" : token})

time.sleep(seconds)

response3 = requests.get(URL, params={"token" : token})

print(response3.status_code, response3.text)