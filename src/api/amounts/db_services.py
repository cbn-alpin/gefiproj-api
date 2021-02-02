from flask import Blueprint, current_app
from src.shared.entity import Session
from ..receipts.entities import Receipt, ReceiptSchema
from .entities import Amount, AmountSchema
from sqlalchemy import func
from sqlalchemy.orm import join

class AmountDBService:
    @staticmethod
    def check_receipt_exists_by_id(receipt_id: int):
        session = Session()
        existing_receipt = session.query(Receipt).filter_by(id_r=receipt_id).first()
        session.close()
        
        if existing_receipt is None:
            raise ValueError(f'La recette {receipt_id} n\'existe pas.',404)

    @staticmethod
    def check_amount_exists_by_id(amount_id: int):
        session = Session()
        existing_receipt = session.query(Amount).filter_by(id_ma=amount_id).first()
        session.close()
        
        if existing_receipt is None:
            raise ValueError(f'Le montant affecté {amount_id} n\'existe pas.',404)


    @staticmethod
    def get_amount_by_receipt_id(receipt_id: int):
        session = Session()  
        amounts_object = session.query(Amount).filter_by(id_r=receipt_id).all()

        # Transforming into JSON-serializable objects
        schema = AmountSchema(many=True)
        amounts = schema.dump(amounts_object)
        # Serializing as JSON
        session.close()
        return amounts
    
    
    @staticmethod
    def insert(amount):
        posted_amount = AmountSchema(only=('id_r', 'montant_ma', 'annee_ma')).load(amount)
        data = Amount(**posted_amount)
        
        session = Session()
        session.add(data)
        session.commit()

        inserted_amount = AmountSchema().dump(data)
        session.close()
        return inserted_amount


    @staticmethod
    def update(amount):
        posted_amount = AmountSchema(only=('id_ma', 'id_r', 'montant_ma', 'annee_ma')).load(amount)
        data = Amount(**posted_amount)
        
        session = Session()
        session.merge(data)
        session.commit()

        updated_amount = AmountSchema().dump(data)
        session.close()
        return updated_amount


    @staticmethod
    def delete(amount_id: int):
        session = Session()
        amount = session.query(Amount).filter_by(id_ma=amount_id).first()
        session.delete(amount)
        session.commit()
        session.close()
        response = {
            'message': f'Le montant affecté {amount_id} a été supprimé'
        }
        return response
    
    @staticmethod
    def check_sum_value(amount):
        session = Session()     
        diff = -1
        res = []
        # insert
        if 'id_ma' not in amount:
            res = session.execute("select (r.montant_r - COALESCE(sum(ma.montant_ma), 0)) as difference "
                                                        "from recette r left join montant_affecte ma on ma.id_r = r.id_r "
                                                        "where r.id_r=:receipt_id group by r.id_r",
                                                        {'receipt_id': amount['id_r']})
            
        # update
        elif 'id_ma' in amount :
            res = session.execute("select (r.montant_r - COALESCE(sum(ma.montant_ma), 0)) as difference "
                                                        "from recette r left join montant_affecte ma on ma.id_r = r.id_r "
                                                        "where r.id_r=:receipt_id and ma.id_ma=:amount_id group by r.id_r",
                                                        {'receipt_id': amount['id_r'], 'amount_id': amount['id_ma']})        
                    
        if res is not None: 
            rest_amounts = 0
            for r in res:
                rest_amounts = float(r['difference'])
            diff = rest_amounts + float(amount['montant_ma'])
        
        session.close()
        return diff >= 0
    
    
    @staticmethod
    def check_error_sum_value(amount):
        if AmountDBService.check_sum_value(amount) == False:
            raise ValueError(f'Erreur de valeur: la somme des montants affectés est supérieur au montant de sa recette.',422)
