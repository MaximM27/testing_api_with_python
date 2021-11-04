import pytest
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class Test_user_register(BaseCase):
    exclude_fields = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_value_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, f"Users with email '{email}' already exists",
                                            f"Unexpected response content {response.content}")

    def test_create_user_with_email_without_at(self):
        email = 'testexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_has_value(response, "Invalid email format",
                                            f"Unexpected response content {response.content}")

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