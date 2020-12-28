from flask import Blueprint, current_app
from src.shared.entity import Session
from ..receipts.entities import Receipt, ReceiptSchema
from .entities import Amount, AmountSchema


class AmountDBService:
    @staticmethod
    def check_receipt_exists(receipt_id):
        session = Session()
        existing_receipt = session.query(Receipt).filter_by(id_r=receipt_id).first()
        session.close()
        
        if existing_receipt is None:
            raise ValueError(f'La recette {receipt_id} n\'existe pas.',404)


    @staticmethod
    def get_amount_by_receipt_(receipt_id: int):
        session = Session()  
        amounts_object = session.query(Amount).filter_by(id_r=receipt_id).all()

        # Transforming into JSON-serializable objects
        schema = AmountSchema(many=True)
        amounts = schema.dump(amounts_object)
        # Serializing as JSON
        session.close()
        return amounts