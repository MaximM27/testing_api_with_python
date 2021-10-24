import requests


url = "https://playground.learnqa.ru/api/homework_cookie"
response = requests.get(url)
print(dict(response.cookies))


def test_check_cookie_in_response():
      response1 = requests.get(url)
      assert response1.status_code == 200, "Wrong response code"
      assert "HomeWork" in dict(response1.cookies), "There is no requiered cookie in response"
      assert dict(response1.cookies)["HomeWork"] == "hw_value", "There is no requiered cookie in response"

