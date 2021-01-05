import unittest

from src.api.expenses.db_services import ExpenseDBService
from src.api.expenses.entities import Expense, ExpenseSchema
from src.shared.test_base import DBBaseTestCase


class DBServiceTestCase(DBBaseTestCase):
    def test_insert_expense(self):
        expense = Expense(annee_d=2020, montant_d=2345)
        inserted_expense = ExpenseDBService.insert(expense)

        expense_object = self.db.session.query(Expense).filter_by(id_d=expense.id_d).first()
        expense_found = ExpenseSchema().dump(expense_object)
        self.assertEqual(inserted_expense['id_d'], expense_found['id_d'])
        self.assertEqual(inserted_expense['annee_d'], expense.annee_d)
        self.assertEqual(inserted_expense['montant_d'], expense.montant_d)
        self.db.session.query(Expense).filter_by(id_d=expense.id_d).delete()
        self.db.session.commit()


if __name__ == '__main__':
    unittest.main()
