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

    def test_user_wrong_registration(self):
        """Test wrong registration when user doesn't fill fields"""
        response = self.client.post(SIGNUP_URL,

                                    data=json.dumps(

                                        {'username': 'vinc', 'email': 'vinc@mail.com', 'pass': ''}),

                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "All fields are required")

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

    def test_len_of_username(self):
        """ Username shhould not be less than 4 charcters """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'kash', 'email': 'kash@gmail.com', 'password': 'password12'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Username should be atleast 4 characters")

    def test_validity_of_email(self):
        """ Test user should not be able to register with invalid email """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'vincent', 'email': 'vinc', 'password': '1234567890'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"], "Check your email. It should be of the form name@mail.com")

    def test_username_validity(self):
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': '@*_-auth', 'email': 'auth@gmail.com', 'password': '4158741'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid username")

    def test_login(self):
        self.test_user.save()
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'kash', 'password': '123456789'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You have successfully logged in")

    def test_if_user_exists(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'mukami', 'password': 'mukash'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User does not exist. Create a new account!')

    def test_wrong_password(self):
        """Test for authenication when password is wrong
        User should not be able to login
        """
        self.test_user.save()
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'dannyb', 'password': 'andela'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Username or password is wrong.')