import requests

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"

methods = ["GET", "POST", "PUT", "DELETE"]
method_values = ["GET", "POST", "PUT", "DELETE"]

for real_method in methods:
    for param_value in method_values:
        func = getattr(requests, real_method.lower())
        if real_method in ["GET", "DELETE"]:
            response = func(URL, params = {"method" : param_value})
        else:
            response = func(URL, data = {"method" : param_value})
            
        if real_method != param_value and response.text == '{"success":"!"}':
            print('Anomally!', response.text, response.status_code, real_method, param_value)
        else: 
            print(response.text, response.status_code, real_method, param_value )
