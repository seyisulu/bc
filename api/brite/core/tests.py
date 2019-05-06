import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class BaseCase(APITestCase):
    client = APIClient()
    EMAIL = 'tester@b.co'
    PASSWORD = 'tester'
    USERNAME = 'tester'

    def create_user(self, username=None, email=None, password=None):
        username = username or self.USERNAME
        email = email or self.EMAIL
        password = password or self.PASSWORD
        return User.objects.create_user(username, email, password)

    @staticmethod
    def create_superuser(
            username='super', email='super@b.co', password='super'):
        return User.objects.create_superuser(username, email, password)

    def create_user_via_api(self, username=None, email=None, password=None):
        url = reverse('users')
        return self.client.post(
            url,
            data=json.dumps({
                'email': email or self.EMAIL,
                'password': password or self.PASSWORD,
                'username': username or self.USERNAME,
            }),
            content_type='application/json'
        )

    def get_auth_header(self, token=None):
        return {
            'HTTP_AUTHORIZATION': f'Token {token or self.token}',
        }

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
        self.user = self.create_user()
        auth = self.login_user(self.USERNAME, self.PASSWORD).data
        self.token = auth.get('token')


class AuthTest(BaseCase):
    PASSWORD = 'tester'

    def test_user_authentication(self):
        data = self.login_user(self.user.username, self.PASSWORD).data
        self.assertEqual(self.user.email, data.get('email'), 'Email mismatch')


class UserTest(BaseCase):

    def test_user_add(self):
        email = 'addition@b.co'
        username = 'addition'
        password = 'addition'
        data = self.create_user_via_api(username, email, password).data
        self.assertEqual(email, data.get('email'), 'Email mismatch')

    def test_user_detail(self):
        header = self.get_auth_header()
        url = reverse('user', args=[self.user.pk])
        info = self.client.get(url, {}, **header).data
        self.assertEqual(self.EMAIL, info.get('email'), 'Email mismatch')


class RiskTypeTest(BaseCase):
    def test_risk_type_add(self):
        header = self.get_auth_header()
        url = reverse('risk_types')
        data = {
            'name': 'Wahala+',
            'description': 'Non-discriminatory wahala coverage.',
            'field_types': [
                {
                    'kind': 'number',
                    'name': 'Duration (months)',
                },
                {
                    'kind': 'currency',
                    'name': 'Premium',
                },
                {
                    'kind': 'enum',
                    'name': 'Referrer',
                    'options': json.dumps({
                        'values': ['billboard', 'friend', 'web']
                    }),
                },
            ]
        }
        # path, data=data, format=format, content_type=content_type, **extra
        res = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json',
            **header,
        )
        print(f'res: {res}')
        self.assertEqual(self.EMAIL, data.get('email'), 'Email mismatch')
