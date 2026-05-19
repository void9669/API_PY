import json

string_as_json = '{"answer" : "Hello, Uzza!"}'
object = json.loads(string_as_json)

key = "answer"
if key in object:
    print(object[key])
else:
    print(f"Ключа {key} не существует")