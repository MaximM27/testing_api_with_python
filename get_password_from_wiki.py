import requests
from lxml import html


def get_password_list():
    response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
    tree = html.fromstring(response.text)
    locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
    passwords = tree.xpath(locator)
    password_list = []
    for password in passwords:
        password = str(password).strip()
        password_list.append(password)
    new_password_list = list(set(password_list))
    return new_password_list

