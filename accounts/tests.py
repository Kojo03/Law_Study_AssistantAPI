from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creation(self):
        test_password = os.environ.get('TEST_PASSWORD', 'test_secure_pass_123!')
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=test_password
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'member')
        self.assertTrue(user.check_password(test_password))

class AuthAPITest(APITestCase):
    def setUp(self):
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'
        self.profile_url = '/users/me/'
        
    def test_user_registration(self):
        test_password = os.environ.get('TEST_PASSWORD', 'test_secure_pass_123!')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': test_password,
            'password2': test_password
        }
        response = self.client.post(self.register_url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Registration failed: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
    def test_user_login(self):
        test_password = os.environ.get('TEST_PASSWORD', 'test_secure_pass_123!')
        user = User.objects.create_user(
            username='testuser',
            password=test_password
        )
        data = {
            'username': 'testuser',
            'password': test_password
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_user_profile(self):
        test_password = os.environ.get('TEST_PASSWORD', 'test_secure_pass_123!')
        user = User.objects.create_user(
            username='testuser',
            password=test_password
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
