import requests

start_url = "https://playground.learnqa.ru/api/long_redirect"

response = requests.get(start_url, allow_redirects=True)
f_res = response.history[0] 
s_res = response

print(f_res.url)
print(s_res.url)