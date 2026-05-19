import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

data = json.loads(json_text)

if "messages" in data:
    messages_list = data["messages"]
    if len(messages_list) > 1:
        second_message_text = messages_list[1]
        print(second_message_text)
    else:
        print("В ответе меньше двух сообщений")
else:
    print(f"Parameter isn't in response")