import requests
import pytest

url = "/api/homework_header"
response = MyReq.get(url)
print(dict(response.headers))

def test_header():
    response = MyReq.get(url)
    assert response.headers.get('x-secret-homework-header') == 'Some secret value', \
        "Secret header value is incorrect!"