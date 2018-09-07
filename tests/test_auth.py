import json
from .entry import EntryClass

SIGNUP_URL = '/api/v1/auth/signup'
LOGIN_URL = '/api/v1/auth/login'


class TestAuth(EntryClass):
    """ Add tests for Auth """

    def test_user_registration(self):
        """ Test user registration works correcty """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "registration successful, now login")


    def test_max_reg(self):
        """ Test User cannot register twice """
        self.client.post(SIGNUP_URL,
                         data=json.dumps(self.user_data), content_type='application/json')
        response2 = self.client.post(SIGNUP_URL,
                                     data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response2.status_code, 203)
        result = json.loads(response2.data.decode())
        self.assertEqual(result["message"], "User already exists")

    def test_len_of_pass(self):
        """ Registration password should not be less than 8 characters """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'faith', 'email': 'faith@mail.com', 'password': '123'}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

        result = json.loads(response.data.decode())

        self.assertEqual(result["message"],
                         "Password should be atleast 8 characters")


    def test_username_validity(self):
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': '@*_-auth', 'email': 'auth@gmail.com', 'password': '4158741'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid username")
