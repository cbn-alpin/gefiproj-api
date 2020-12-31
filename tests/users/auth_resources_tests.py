import unittest

from src.api import create_api
from src.api.users.auth_resources import resources
from src.shared import config

TEST_TOKEN = config.get_test_token()


class RessourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_api('test')
        self.app.register_blueprint(resources)
        self.tester = self.app.test_client(self)

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
