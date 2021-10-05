import requests
print('hello from Max')

response = requests.get("https://playground.learnqa.ru/api/hello")
print(response.text)

