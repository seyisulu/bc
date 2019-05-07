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
    DATA = {
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

    def create_risk_type(self, data=None):
        data = data or self.DATA
        return self.client.post(
            reverse('risk_types'),
            data=json.dumps(data),
            content_type='application/json',
            **(self.get_auth_header()),
        ).data

    def test_risk_type_add(self):
        res = self.create_risk_type()
        name = self.DATA.get('name')
        self.assertEqual(res.get('name'), name, 'RiskType mismatch')

    def test_risk_type_get(self):
        dat = self.create_risk_type()
        url = reverse('risk_type', args=[dat.get('pk')])
        header = self.get_auth_header()
        res = self.client.get(url, **header).data
        sent_fields = len(dat.get('field_types', []))
        got_fields = len(res.get('field_types', []))
        self.assertEqual(dat.get('name'), res.get('name'), 'RiskType mismatch')
        self.assertEqual(sent_fields, got_fields, 'FieldType count mismatch')

    def test_risk_type_list(self):
        self.create_risk_type()
        url = reverse('risk_types')
        header = self.get_auth_header()
        res = self.client.get(url, **header).data
        self.assertEqual(res.get('count'), 1, 'RiskType count mismatch')


class RiskTest(BaseCase):
    DATA = {
        'client': 'Baba Iyabo',
        'fields': {
            'Duration (months)': 24,
            'Premium': 1234,
            'Referrer': 'web',
        }
    }

    def create_risk(self):
        risk_test = RiskTypeTest()
        risk_test.token = self.token
        risk_type = risk_test.create_risk_type()
        data = dict(self.DATA)
        data['risk_type'] = risk_type.get('pk')
        fields = [
            {
                'field_type': field_type['pk'],
                'value': data['fields'][field_type['name']],
            }
            for field_type in risk_type['field_types']
        ]
        data['fields'] = fields
        return self.client.post(
            reverse('risks'),
            data=json.dumps(data),
            content_type='application/json',
            **(self.get_auth_header()),
        ).data

    def test_risk_add(self):
        risk = self.create_risk()
        client = self.DATA['client']
        self.assertEqual(client, risk.get('client'), 'Risk mismatch')

    def test_risk_get(self):
        risk = self.create_risk()

        url = reverse('risk', args=[risk.get('pk')])
        header = self.get_auth_header()
        res = self.client.get(url, **header).data

        sent_fields = len(risk.get('fields', []))
        got_fields = len(res.get('fields', []))
        client = res.get('client')

        self.assertEqual(risk.get('client'), client, 'Risk mismatch')
        self.assertEqual(sent_fields, got_fields, 'Field count mismatch')

    def test_risk_list(self):
        self.create_risk()
        self.create_risk()

        url = reverse('risks')
        header = self.get_auth_header()
        res = self.client.get(url, **header).data

        self.assertEqual(res.get('count'), 2, 'Risk count mismatch')
