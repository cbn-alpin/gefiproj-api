from flask import current_app
from src.api.expenses.entities import Expense, ExpenseSchema
from src.shared.entity import Session
from sqlalchemy import desc
from src.shared.manage_error import CodeError, ManageErrorUtils, TError


class ExpenseDBService:
    @staticmethod
    def get_all_expenses():
        session = None
        response = []
        try:
            session = Session()  
            expenses_object = session.query(Expense).order_by(Expense.annee_d.desc()).all()
            # Transforming into JSON-serializable objects
            schema = ExpenseSchema(many=True)
            expenses = schema.dump(expenses_object)
            
            session.close()
            return expenses
        except Exception as error:
            current_app.logger.error(f"ExpenseDBService - get_all_expenses : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ExpenseDBService - get_all_expenses : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_unique_year(year: int, expense_id = None):
        session = None
        response = None
        try:
            session = Session()  
            if expense_id is not None:
                response = session.query(Expense).filter(Expense.id_d != expense_id, Expense.annee_d == year).first()
            else:
                response = session.query(Expense).filter_by(annee_d=year).first()
 
            if response is not None:
                msg = "La dépense de l\'année '{}' est déjà utilisé sur une autre dépense".format(year)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 409)

            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"ExpenseDBService - check_unique_year : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ExpenseDBService - check_unique_year : {error}")
            raise
        finally:
            if session is not None:
                session.close()      
        
    @staticmethod
    def insert(expense):
        session = None
        update_funder = None
        try:
            # save expense
            posted_expense = ExpenseSchema(only=('annee_d', 'montant_d')).load(expense)
            expense = Expense(**posted_expense)
            
            session = Session()
            session.add(expense)
            session.commit()
            
            new_expense = ExpenseSchema().dump(expense)
            session.close()
            return new_expense
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - insert : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(expense):
        session = None
        update_funder = None
        try:
            data = ExpenseSchema(only=('id_d', 'annee_d', 'montant_d')).load(expense)
            expense = Expense(**data)
            
            session = Session()
            session.merge(expense)
            session.commit()
            
            update_funder = ExpenseSchema().dump(expense)
            session.close()
            return update_funder
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - update : {error}")
            raise
        finally:
            if session is not None:
                session.close()        
    
    @staticmethod
    def delete(expense_id: int, year: int):
        session = None
        try:
            session = Session()
            data = session.query(Expense).filter_by(id_d=expense_id).delete()
            session.commit()
             
            session.close()
            return { 'message': 'La dépense de l\'année \'{}\' a été supprimé'.format(year) }
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ExpenseDBService - delete : {error}")
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_expense_by_id(expense_id: int):
        session = None
        response = None
        try:
            session = Session()  
            expense = session.query(Expense).filter_by(id_d=expense_id).first()

            if expense is None:
                msg = "La dépense n'existe pas"
                ManageErrorUtils.value_error(CodeError.DB_VALUE_REFERENCED, TError.DATA_NOT_FOUND, msg, 404)
            
            schema = ExpenseSchema()
            response = schema.dump(expense)
            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"ExpenseDBService - get_expense_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ExpenseDBService - get_expense_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()
