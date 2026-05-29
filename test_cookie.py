import requests
import pytest

url = "/api/homework_cookie"

def test_cookie():
    response = MyReq.get(url)
    cookiename = response.cookies['HomeWork']
    assert cookiename == "hw_value" , "Cookie isn't correct!"
