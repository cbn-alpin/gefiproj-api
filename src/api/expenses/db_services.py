from src.api.expenses.entities import Expense, ExpenseSchema
from src.shared.entity import Session
from sqlalchemy import desc

class ExpenseDBService:
    @staticmethod
    def get_all_expenses():
        session = Session()  
        expenses_object = session.query(Expense).order_by(Expense.annee_d.desc()).all()
        # Transforming into JSON-serializable objects
        schema = ExpenseSchema(many=True)
        expenses = schema.dump(expenses_object)
        # Serializing as JSON
        session.close()
        return expenses
    
    @staticmethod
    def insert(expense):
        # save expense
        posted_expense = ExpenseSchema(only=('annee_d', 'montant_d')).load(expense)
        data = Expense(**posted_expense)
        
        session = Session()
        session.add(data)
        session.commit()

        inserted_expense = ExpenseSchema().dump(data)
        session.close()
        return inserted_expense

    @staticmethod
    def update(expense):
        update_expense = ExpenseSchema(only=('id_d', 'annee_d', 'montant_d')).load(expense)
        data = Expense(**update_expense)
        
        session = Session()
        session.merge(data)
        session.commit()

        update_expense = ExpenseSchema().dump(data)
        session.close()
        return update_expense
    
    @staticmethod
    def delete(expense_id: int):
        session = Session()
        expense = session.query(Expense).filter_by(id_d=expense_id).first()
        session.delete(expense)
        session.commit()
        session.close()
        response = {
            'message': f'La dépense de l\'année {expense.annee_d} a été supprimé.'
        }
        return response
    
    @staticmethod
    def check_exist_expense(expense_id: int):
        session = Session()  
        expense_existing = session.query(Expense).filter_by(id_d=expense_id).first()
        session.close()
        
        if expense_existing is None:
            raise ValueError(f'La dépense {expense_id} n\'existe pas.',404)
   
    @staticmethod
    def check_unique_year(year: int):
        session = Session()  
        expense_existing = session.query(Expense).filter_by(annee_d=year).first()
        session.close()
        
        if expense_existing is not None:
            raise ValueError(f'La dépense de l\'année {year} existe déjà.',404)