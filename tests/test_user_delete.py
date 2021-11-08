import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.description("This test try to delete test user who can't be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_with_id_2(self):
        # Login
        with allure.step("Login user"):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response1 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id = self.get_json_value(response1, "user_id")

        # Delete
        with allure.step("Try to delete user"):
            response2 = MyRequests.delete(f"/user/{user_id}",
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid})

            Assertions.assert_code_status(response2, 400)
            Assertions.assert_content_has_value(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                                                f"Unexpected response content {response2.content}")

    @allure.description("This test try to get deleted user data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_try_to_get_deleted_user_data(self):
        # Register
        with allure.step("Register user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_value_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        # Login
        with allure.step("Login user"):
            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # Delete
        with allure.step("Try to delete user"):

            response3 = MyRequests.delete(f"/user/{user_id}", headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})

            Assertions.assert_code_status(response3, 200)

        # Get
        with allure.step("Try to get user data"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       )
            Assertions.assert_code_status(response4, 404)
            Assertions.assert_content_has_value(response4, "User not found", f"Unexpected response content {response4.content}")

    @allure.description("This test try to delete user with auth by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_auth_by_another_user(self):
        # Register 1st user
        with allure.step("The 1st user registration"):
            register_data1 = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data1)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_value_has_key(response1, "id")

            email1 = register_data1['email']
            password1 = register_data1['password']

        # Register 2nd user
        with allure.step("The 2st user registration"):
            register_data2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=register_data2)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_value_has_key(response2, "id")

            user_id2 = self.get_json_value(response2, 'id')

        # Login by 1st user
        with allure.step("The 2st user login"):
            login_data1 = {
                'email': email1,
                'password': password1
            }

            response3 = MyRequests.post("/user/login", data=login_data1)

            auth_sid1 = self.get_cookie(response3, "auth_sid")
            token1 = self.get_header(response3, "x-csrf-token")

        # Delete 2nd user
        with allure.step("Try to delete 2nd user"):
            response3 = MyRequests.delete(f"/user/{user_id2}", headers={'x-csrf-token': token1}, cookies={'auth_sid': auth_sid1})
            Assertions.assert_code_status(response3, 200)

        # Get 2nd user data
        with allure.step("Try to get 2nd user data"):
            response4 = MyRequests.get(f"/user/{user_id2}")
            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_has_key(response4, "username")

