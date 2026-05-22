import requests
import pytest

url = "https://playground.learnqa.ru/api/homework_header"
response = requests.get(url)
print(dict(response.headers))

def test_header():
    response = requests.get(url)
    assert response.headers.get('x-secret-homework-header') == 'Some secret value', \
        "Secret header value is incorrect!"