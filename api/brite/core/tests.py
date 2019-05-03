import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class BaseCase(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username='tester', email='tester@b.co', password='tester'):
        return User.objects.create_user(username, email, password)

    @staticmethod
    def create_superuser(
            username='super', email='super@b.co', password='super'):
        return User.objects.create_superuser(username, email, password)

    def login_user(self, username, password):
        url = reverse('auth')
        return self.client.post(
            url,
            data=json.dumps({
                'username': username,
                'password': password,
            }),
            content_type='application/json'
        )

    def setUp(self):
        # create a user
        self.user = self.create_user()
        # TODO: add test data (setUpTestData)


class AuthTest(BaseCase):
    PASSWORD = 'tester'

    def test_user_authentication(self):
        data = self.login_user(self.user.username, self.PASSWORD).data
        self.assertEqual(self.user.email, data.get('email'), 'Email mismatch')


class UserTest(BaseCase):
    EMAIL = 'addition@b.co'
    PASSWORD = 'addition'
    USERNAME = 'addition'

    def create_user_via_api(self):
        url = reverse('user-add')
        return self.client.post(
            url,
            data=json.dumps({
                'email': self.EMAIL,
                'password': self.PASSWORD,
                'username': self.USERNAME,
            }),
            content_type='application/json'
        )

    def test_user_add(self):
        data = self.create_user_via_api().data
        self.assertEqual(self.EMAIL, data.get('email'), 'Email mismatch')

    def test_user_detail(self):
        data = self.create_user_via_api().data
        pk = data.get('url', '').split('/')[-1]
        url = reverse('user-detail', args=[pk])
        auth = self.login_user(self.USERNAME, self.PASSWORD).data
        token = auth.get('token')
        header = {'HTTP_AUTHORIZATION': f'Token {token}'}
        info = self.client.get(url, {}, **header).data
        self.assertEqual(self.EMAIL, info.get('email'), 'Email mismatch')
