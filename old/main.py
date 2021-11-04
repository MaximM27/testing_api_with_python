import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

url = response.url
q = len(response.history)
#print(f"Количество редиректов равно {q}")
#print(f"Конечный url запроса: {url}")

text = response.json()
print(text)