import pytest
import allure
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User registration cases")
class Test_user_register(BaseCase):
    exclude_fields = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    @allure.description("This test successfully create user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_value_has_key(response, "id")

    @allure.description("This test try to create user with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, f"Users with email '{email}' already exists",
                                            f"Unexpected response content {response.content}")

    @allure.description("This test try to create with user with invalid email without at")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_email_without_at(self):
        email = 'testexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, "Invalid email format",
                                            f"Unexpected response content {response.content}")

    @allure.description("This test try to create user without requiered fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('field', exclude_fields)
    def test_create_user_without_required_field(self, field):
        data = self.prepare_registration_data()
        try:
            del data[field]
        except KeyError:
            pass

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, f"The following required params are missed: {field}",
                                            f"Unexpected response content {response.content}")

    @allure.description("This test try to create user with short name")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        try:
            data['username'] = 'a'
        except KeyError:
            pass

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, "The value of 'username' field is too short",
                                            f"Unexpected response content {response.content}")

    @allure.description("This test try to create user without long name")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        try:
            data['username'] = "".join([random.choice(string.ascii_letters) for i in range(260)])
        except KeyError:
            pass

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, "The value of 'username' field is too long",
                                            f"Unexpected response content {response.content}")