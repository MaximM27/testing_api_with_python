from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import random
import allure


@allure.epic("Get user data cases")
class TestUserGet(BaseCase):
    def create_login_request_by_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=data)
        return response

    @allure.description("This test try to get user details without auth data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_value_has_key(response, "username")
        Assertions.assert_json_value_has_not_key(response, "email")
        Assertions.assert_json_value_has_not_key(response, "firstName")
        Assertions.assert_json_value_has_not_key(response, "lastName")

    @allure.description("This test try to get user details with auth as same user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_same_user(self):

        response1 = self.create_login_request_by_user()
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_value_has_keys(response2, expected_fields)

    @allure.description("This test try to get user details with auth as another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_another_user(self):

        response1 = self.create_login_request_by_user()

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        another_user_id = random.randint(user_id_from_auth_method+1, 10000)

        response2 = MyRequests.get(f"/user/{another_user_id}",
                                   headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})

        expected_fields = ['username']
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_value_has_keys(response2, expected_fields)