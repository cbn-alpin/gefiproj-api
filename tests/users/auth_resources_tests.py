import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.users.auth_resources import resources
from src.shared import config

TEST_TOKEN = config.get_test_token()


class RessourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_api('test')

        self.db = SQLAlchemy()
        self.db.app = self.app

        self.app.register_blueprint(resources)
        self.tester = self.app.test_client(self)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_login(self):
        payload = {
            'login': 'testmaill@mail.ml',
            'password': 'admin'
        }
        resp200 = self.tester.post('/api/auth/login',
                                   headers={'content_type': 'application/json',
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=payload)
        response_json = resp200.get_json()
        self.assertEqual(resp200.status_code, 200)
        self.assertEqual(response_json['email_u'], 'testmaill@mail.ml')

    def test_add_user_invalid_data(self):
        invalid_user_data = {'nom_u': 'Samaké', 'prenom_u': 'Zantiè', 'initiales_u': 'zas',
                             'email_u': 'zantie.samake@mail', 'active_u': True,
                             'password_u': 'zan@password', 'roles': []}
        resp422 = self.tester.post('/api/auth/register',
                                   headers={'content_type': 'application/json',
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=invalid_user_data)

        self.assertEqual(resp422.status_code, 422)

    def test_add_user_ok(self):
        new_user = {'nom_u': 'Samaké', 'prenom_u': 'Zantiè', 'initiales_u': 'zas',
                    'email_u': 'zantie.samake@mail.ml',
                    'password_u': 'zan@password', 'active_u': True, 'roles': ['consultant']}
        resp201 = self.tester.post('/api/auth/register',
                                   headers={'content_type': 'application/json',
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=new_user)
        response_json = resp201.get_json()

        self.assertEqual(resp201.status_code, 201)
        self.assertFalse('password_u' in response_json)
        self.assertEqual(response_json['initiales_u'], 'zas')
