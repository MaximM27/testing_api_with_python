import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
token = json.loads(response.text)['token']
time_to_finish = json.loads(response.text)['seconds']


def get_request(param):
    get_response = requests.get(url, params={'token': param})
    return get_response


response1 = get_request(token)
if response1.text == '{"error": "No job linked to this token"}':
    print("Can't find a job for this token")
elif json.loads(response1.text)['status'] == 'Job is NOT ready':
    time.sleep(time_to_finish)
    response2 = get_request(token)
    if json.loads(response2.text)['status'] == 'Job is ready':
        result = json.loads(response2.text)['result']
        print(f"Результат выполнения задачи: {result}")
elif json.loads(response1.text)['status'] == 'Job is ready':
    result = json.loads(response1.text)['result']
    print(f"Результат выполнения задачи: {result}")
