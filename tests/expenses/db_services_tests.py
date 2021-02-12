import unittest

from src.api.expenses.db_services import ExpenseDBService
from src.api.expenses.entities import Expense, ExpenseSchema
from src.shared.test_base import DBBaseTestCase


class DBServiceTestCase(DBBaseTestCase):
    def test_insert_expense(self):
        expense = {'annee_d': 2020, 'montant_d': 2345}
        inserted_expense = ExpenseDBService.insert(expense)

        expense_object = self.db.session.query(Expense).filter_by(id_d=inserted_expense.get('id_d')).first()
        expense_found = ExpenseSchema().dump(expense_object)
        self.assertEqual(inserted_expense.get('id_d'), expense_found.get('id_d'))
        self.assertEqual(inserted_expense.get('annee_d'), expense.get('annee_d'))
        self.assertEqual(inserted_expense.get('montant_d'), expense.get('montant_d'))
        self.db.session.query(Expense).filter_by(id_d=expense.get('id_d')).delete()
        self.db.session.commit()

    def test_get_all_expenses(self):
        self.db.session.bulk_save_objects([
            Expense(annee_d=2020, montant_d=2345),
            Expense(annee_d=2021, montant_d=7395)
        ])
        self.db.session.commit()

        expenses = ExpenseDBService.get_all_expenses()
        self.assertEqual(len(expenses), 2)

    def test_update(self):
        expense = Expense(annee_d=2020, montant_d=2345)
        self.db.session.add(expense)
        self.db.session.commit()

        expense.annee_d = 2019
        expense_object = ExpenseSchema().dump(expense)
        expense = ExpenseDBService.update(expense_object)

        self.assertEqual(expense['annee_d'], 2019)

    def test_delete(self):
        expense = Expense(annee_d=2020, montant_d=2345)
        self.db.session.add(expense)
        self.db.session.commit()

        ExpenseDBService.delete(expense.id_d, 2020)
        expense_found = self.db.session.query(Expense).filter_by(id_d=expense.id_d).first()
        self.assertEqual(expense_found, None)

    def test_get_expense_by_id(self):
        expense = Expense(annee_d=2020, montant_d=2345)
        self.db.session.add(expense)
        self.db.session.commit()

        expense_found = ExpenseDBService.get_expense_by_id(expense.id_d)
        self.assertEqual(expense_found['annee_d'], 2020)
        self.assertEqual(expense_found['montant_d'], 2345)


if __name__ == '__main__':
    unittest.main()
