import requests
import pytest

url = "https://playground.learnqa.ru/api/homework_cookie"

def test_cookie():
    response = requests.get(url)
    cookiename = response.cookies['HomeWork']
    assert cookiename == "hw_value" , "Cookie isn't correct!"
