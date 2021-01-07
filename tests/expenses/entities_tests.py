import unittest

from src.api.expenses.entities import Expense, ExpenseSchema


class EntitiesTestCase(unittest.TestCase):
    def test_expense_entity(self):
        expense = Expense(2010, 3575.39)
        self.assertEqual(expense.id_d, None)
        self.assertEqual(expense.annee_d, 2010)
        self.assertEqual(expense.montant_d, 3575.39)

    def test_expense_schema(self):
        schema = ExpenseSchema()
        data = schema.load({'annee_d': '2022', 'montant_d': '990.5'})
        expense = Expense(**data)

        self.assertEqual(expense.id_d, None)
        self.assertEqual(expense.annee_d, 2022)
        self.assertEqual(expense.montant_d, 990.5)


if __name__ == '__main__':
    unittest.main()
