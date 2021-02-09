from flask import current_app
from src.shared.manage_error import CodeError, ManageErrorUtils, TError

from src.shared.entity import Session
from ..receipts.entities import Receipt
from .entities import Amount, AmountSchema
from sqlalchemy import func
from sqlalchemy.orm import join


class AmountDBService:
    @staticmethod
    def get_amount_by_receipt_id(receipt_id: int):
        session = None
        response = None
        try:
            session = Session()  
            amounts = []
            amounts = session.query(Amount).filter_by(id_r=receipt_id).all()

            # Transforming into JSON-serializable objects
            schema = AmountSchema(many=True)
            amounts = schema.dump(amounts)
            # Serializing as JSON
            session.close()
            return amounts
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def insert(amount):
        session = None
        new_amount = None
        try:
            posted_amount = AmountSchema(only=('id_r', 'montant_ma', 'annee_ma')).load(amount)
            amount = Amount(**posted_amount)
            
            session = Session()
            session.add(amount)
            session.commit()
            
            if amount is None:
                msg = "Une erreur est survenue lors de l'enregistrement du montant affecté"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.INSERT_ERROR, msg, 404)


            new_amount = AmountSchema().dump(amount)
            session.close()
            return new_amount
        except ValueError as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(amount):
        session = None
        updated_amount = None
        try:
            data = AmountSchema(only=('id_ma', 'id_r', 'montant_ma', 'annee_ma')).load(amount)
            amount = Amount(**data)
            
            session = Session()
            session.merge(amount)
            session.commit()
            
            if amount is None:                
                msg = "Une erreur est survenue lors de la modification du montant affecté"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.UPDATE_ERROR, msg, 404)
           
            updated_amount = AmountSchema().dump(amount)
            session.close()
            return updated_amount
        except (Exception, ValueError) as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()  

    @staticmethod
    def delete(amount_id: int):
        session = None
        try:
            session = Session()
            data = session.query(Amount).filter_by(id_ma=amount_id).delete()
            session.commit()
            
            if data is None:                
                msg = "Une erreur est survenue lors de la suppression du montant affecté"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DELETE_ERROR, msg, 404)
           
            session.close()
            return { 'message': 'Le montant affecté de l\'année a été supprimé' }
        except (Exception, ValueError) as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def check_sum_value(amount, amount_id: int = None):
        session = None
        response = []
        try:
            session = Session()     
            diff = -1
            if amount_id is None:
                # check insert
                response = session.query(Receipt, \
                    ( Receipt.montant_r - func.coalesce(func.sum(Amount.montant_ma), 0) ).label('difference') ) \
                    .join(Amount, Receipt.id_r == Amount.id_r, isouter=True) \
                    .filter(Receipt.id_r == amount['id_r']) \
                    .group_by(Receipt.id_r)
            else:
                # check update
                response = session.query(Receipt, \
                    ( Receipt.montant_r - func.coalesce(func.sum(Amount.montant_ma), 0) ).label('difference') ) \
                    .join(Amount, Receipt.id_r == Amount.id_r, isouter=True) \
                    .filter(Receipt.id_r == amount['id_r'], Amount.id_ma != amount_id) \
                    .group_by(Receipt.id_r)
            
            print(response)
            if response is not None or len(response) > 0: 
                rest_amounts = 0
                for r in response:
                    rest_amounts = float(r['difference'])
                if amount_id is None:
                    diff = rest_amounts
                else:
                    diff = rest_amounts - float(amount['montant_ma'])
            
            if diff < 0:
                msg = "Erreur de valeur: la somme des montants affectés est supérieur au montant de sa recette."
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, msg, 422)

            session.close()
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()      
    
    # TODO remove
    @staticmethod
    def delete_amounts_by_receipt_id(receipt_id: int):
        session = Session()
        delete_amounts = Amount.__table__.delete().where(Amount.id_r==receipt_id)
        session.execute(delete_amounts)
        
        session.commit()
        session.close()
        
    @staticmethod
    def check_unique_amount_by_year_and_receipt_id(year: int, receipt_id: int, amount_id = None):
        session = None
        response = None
        try:
            session = Session()  
            if amount_id is not None:
                response = session.query(Amount) \
                    .filter(Amount.id_ma != amount_id, Amount.id_r == receipt_id, Amount.annee_ma == year) \
                    .first()
            else:
                response = session.query(Amount) \
                    .filter_by(id_r=receipt_id, annee_ma=year) \
                    .first()
                    
            if response is not None:
                msg = "L\'année {} du montant affecté de cette recette est déjà utilisé sur un autre montant affecté".format(year)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 409)

            session.close()
            return response
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()      
        