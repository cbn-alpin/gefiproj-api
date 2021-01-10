from src.shared.entity import Session
from .entities import Receipt, ReceiptSchema
from ..fundings.entities import Funding


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.',404)

    @staticmethod
    def get_receipts_by_funding_id(funding_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_f=funding_id).all()

        # Transforming into JSON-serializable objects
        schema = ReceiptSchema(many=True)
        receipt = schema.dump(receipt_object)
        # Serializing as JSON
        session.close()
        return receipt

    @staticmethod
    def get_receipt_by_id(receipt_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_r=receipt_id).first()

        schema = ReceiptSchema()
        receipt = schema.dump(receipt_object)
        session.close()

        return receipt

    @staticmethod
    def insert(receipt: Receipt):
        session = Session()
        session.add(receipt)
        session.commit()

        inserted_receipt = ReceiptSchema().dump(receipt)
        session.close()
        return inserted_receipt

    @staticmethod
    def check_receipt_exists_by_id(receipt_id: int):
        existing_receipt = ReceiptDBService.get_receipt_by_id(receipt_id)
        if not existing_receipt:
            msg = {
                'code': 'RECEIPT_NOT_FOUND',
                'message': f'Receipt with id <{receipt_id}> does not exist.'
            }

            return msg
