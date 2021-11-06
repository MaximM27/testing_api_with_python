from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        #Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        #Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 data={'firstName': new_name})

        Assertions.assert_code_status(response3, 200)

        #Get
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 )
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    def test_edit_user_without_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_has_key(response1, "id")

        user_id = self.get_json_value(response1, 'id')

        # Edit
        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content_has_value(response3, "Auth token not supplied",
                                            f"Unexpected response content {response3.content}")

    def test_edit_user_auth_by_another_user(self):
        # Register 1st user
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_has_key(response1, "id")

        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
        password1 = register_data1['password']
        user_id1 = self.get_json_value(response1, 'id')

        # Register 2nd user
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_value_has_key(response2, "id")

        email2 = register_data2['email']
        first_name2 = register_data2['firstName']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response2, 'id')

        # Login by 1st user
        login_data1 = {
            'email': email1,
            'password': password1
        }

        response3 = MyRequests.post("/user/login", data=login_data1)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # Edit 2nd user data
        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id2}",
                                   headers={'x-csrf-token': token1},
                                   cookies={'auth_sid': auth_sid1},
                                   data={'firstName': new_name})
        # Login by 2nd user
        login_data2 = {
            'email': email2,
            'password': password2
        }

        response4 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        Assertions.assert_code_status(response4, 200)

        # Get 2nd user data
        response5 = MyRequests.get(f"/user/{user_id2}",
                                   headers={'x-csrf-token': token2},
                                   cookies={'auth_sid': auth_sid2},
                                   )
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(response5, "firstName", first_name2, "Wrong name of the user after edit")

    def test_edit_user_email_without_at(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_email = email.replace('@', '')

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_email})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content_has_value(response3, "Invalid email format", f"Unexpected response content {response3.content}")

    def test_edit_user_with_short_firstname(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_firstname = first_name[1]

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_firstname})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName", f"Unexpected response text{response3.text}")
