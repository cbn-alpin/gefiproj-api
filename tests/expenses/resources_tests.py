import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.expenses.entities import Expense
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

    def test_add_expense(self):
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
        self.db.session.query(Expense).filter_by(id_d=response_json['id_d']).delete()
        self.db.session.commit()

    def test_get_expenses(self):
        self.db.session.query(Expense).delete()
        expense = Expense(2020, 2020)
        self.db.session.add(expense)
        self.db.session.commit()
        resp200 = self.tester.get('/api/expenses',
                                  headers={'content_type': 'application/json',
                                           'Authorization': f'Bearer {TEST_TOKEN}'})
        response_json = resp200.get_json()

        self.assertEqual(resp200.status_code, 200)
        self.assertEqual(len(response_json), 1)
        self.db.session.query(Expense).filter_by(id_d=expense.id_d).delete()
        self.db.session.commit()

    def test_update_expense(self):
        expense = Expense(2022, 2020)
        self.db.session.add(expense)
        self.db.session.commit()

        new_expense = {'id_d': expense.id_d, 'annee_d': 2009, 'montant_d': 409.698}
        resp200 = self.tester.put(f'/api/expenses/{expense.id_d}',
                                  headers={'content_type': 'application/json',
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=new_expense)
        response_json = resp200.get_json()

        self.assertEqual(resp200.status_code, 200)
        self.assertTrue('id_d' in response_json)
        self.assertTrue('annee_d' in response_json)
        self.assertEqual(response_json['montant_d'], 409.698)
        self.db.session.query(Expense).filter_by(id_d=expense.id_d).delete()
        self.db.session.commit()

    def test_delete_expense(self):
        expense = Expense(2021, 7010)
        self.db.session.add(expense)
        self.db.session.commit()

        resp204 = self.tester.delete(f'/api/expenses/{expense.id_d}',
                                     headers={'content_type': 'application/json',
                                              'Authorization': f'Bearer {TEST_TOKEN}'})
        self.assertEqual(resp204.status_code, 204)
