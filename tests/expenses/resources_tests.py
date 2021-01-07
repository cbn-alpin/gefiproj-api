import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.expenses.resources import resources as expense_resources
from src.shared import config

TEST_TOKEN = config.get_test_token()


class RessourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_api('test')

        self.db = SQLAlchemy()
        self.db.app = self.app

        self.app.register_blueprint(expense_resources)
        self.tester = self.app.test_client(self)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_insert_expense_ok(self):
        new_expense = {'annee_d': 2009, 'montant_d': 409.698}
        resp201 = self.tester.post('/api/expenses',
                                   headers={'content_type': 'application/json',
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=new_expense)
        response_json = resp201.get_json()

        self.assertEqual(resp201.status_code, 201)
        self.assertTrue('id_d' in response_json)
        self.assertTrue('annee_d' in response_json)
        self.assertEqual(response_json['montant_d'], 409.698)
