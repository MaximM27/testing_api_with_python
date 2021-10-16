import requests

response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
response2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
response3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
responses = [response1, response2, response3]
for i in responses:
    print(f'{responses.index(i)+1})Код ответа: {i.status_code} \n   Текст ответа: {i.text}')

def all_requests(param):
    get_response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": param})
    post_response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": param})
    put_response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": param})
    delete_response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": param})
    all_responses = [get_response, post_response, put_response, delete_response]
    for j in all_responses:
        if param == j.request.method:
            if j.status_code == 200 and j.text == '{"success":"!"}':
                pass
            else:
                print(f'При совпадении типа запроса и параметра в DELETE-запросе сервер отвечает c ошибкой: \n   Код ответа: {j.status_code} \n   Текст ответа: {j.text}')
        elif param != j.request.method:
            if j.status_code == 200 and j.text == '{"success":"!"}':
                print(
                    f'Ошибка! Некорректная обработка серверсом DELETE-запроса с парметром {param} : \n   Код ответа: {j.status_code} \n   Текст ответа: {j.text}')


print('4) Проверка комбинаций методов и параметров:')
methods = ['GET', 'POST', 'PUT', 'DELETE']

for i in methods:
    all_requests(i)