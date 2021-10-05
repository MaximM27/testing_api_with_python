import requests
print('hello from Max')

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

