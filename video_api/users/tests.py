from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "password": "validPassword123",
            "password2": "validPassword123",
            "email": "testuser@example.com",
            "is_staff": False,
        }

    def test_user_registration_with_valid_data(self):
        response = self.client.post('/register/', self.valid_data)
        print(response.data)  # type: ignore
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)  # type: ignore
        self.assertIn('username', response.data)  # type: ignore
        self.assertIn('email', response.data)  # type: ignore
        self.assertIn('refresh', response.data)  # type: ignore
        self.assertIn('access', response.data)  # type: ignore
        self.assertEqual(response.data['username'], self.valid_data['username'])  # type: ignore
        self.assertEqual(response.data['email'], self.valid_data['email'])  # type: ignore


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            password="validPassword123",
            email="validemail@example.com",
            is_staff=False
        )

    def test_user_login_with_valid_credentials(self):
        response = self.client.post('/login/', {
            'username': self.user.username,
            'password': 'validPassword123'
        })
        print(response.data)  # type: ignore
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.data)  # type: ignore
        self.assertIn('email', response.data)  # type: ignore
        self.assertIn('refresh', response.data)  # type: ignore
        self.assertIn('access', response.data)  # type: ignore
        self.assertEqual(response.data['username'], self.user.username)  # type: ignore
        self.assertEqual(response.data['email'], self.user.email)  # type: ignore
