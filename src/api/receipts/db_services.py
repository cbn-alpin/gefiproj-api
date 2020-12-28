from flask import Blueprint, current_app
from src.shared.entity import Session
from ..fundings.entities import Funding, FundingSchema
from .entities import Receipt, ReceiptSchema


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.',404)


    @staticmethod
    def get_receipts_by_funding(funding_id: int):
        session = Session()  
        receipt_object = session.query(Receipt).filter_by(id_f=funding_id).all()

        # Transforming into JSON-serializable objects
        schema = ReceiptSchema(many=True)
        receipt = schema.dump(receipt_object)
        # Serializing as JSON
        session.close()
        return receipt