import requests


url = "https://playground.learnqa.ru/api/homework_header"
response = requests.get(url)
print(dict(response.headers))

def test_check_header_in_response():
      response1 = requests.get(url)
      assert response1.status_code == 200, "Wrong response code"
      assert "x-secret-homework-header" in dict(response1.headers), "There is no requiered header in response"
      assert dict(response1.headers)["x-secret-homework-header"] == "Some secret value", "There is no requiered header in response"

