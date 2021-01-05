from src.api.expenses.entities import Expense, ExpenseSchema
from src.shared.entity import Session


class ExpenseDBService:
    @staticmethod
    def insert(expense: Expense):
        session = Session()
        session.add(expense)
        session.commit()

        inserted_expense = ExpenseSchema().dump(expense)
        session.close()
        return inserted_expense
