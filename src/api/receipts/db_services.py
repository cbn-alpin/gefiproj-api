from src.shared.entity import Session
from .entities import Receipt, ReceiptSchema
from sqlalchemy import func

from ..fundings.entities import Funding
from ..projects.entities import Project
from ..amounts.entities import Amount


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.', 404)

    @staticmethod
    def get_receipts_of_year_by_funding_id(funding_id: int or str, year: int or str):
        session = None
        receipts = None

        try:
            session = Session()
            receipts = session.query(Receipt).filter(Receipt.id_f == funding_id, Receipt.annee_r == year).all()
            receipts = ReceiptSchema(many=True).dump(receipts)
        finally:
            session.close()

        return receipts

    @staticmethod
    def get_receipts_by_funding_id(funding_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_f=funding_id).order_by(Receipt.id_r).all()

        rest_receipt_amount_object = session.query(*[c.label(c.name) for c in Receipt.__table__.c ], ( Receipt.montant_r - func.coalesce(func.sum(Amount.montant_ma), 0) ).label('difference')) \
            .join(Amount, Amount.id_r == Receipt.id_r, isouter=True) \
            .filter(Receipt.id_f == funding_id)\
            .group_by(Receipt.id_r)\
            .order_by(Receipt.id_r.desc()) \
            .all()
            
        receipts = []
        for r in rest_receipt_amount_object:
            receipts.append(r._asdict())

        session.close()
        return receipts

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
    def update(receipt: Receipt):
        session = Session()
        session.merge(receipt)
        session.commit()

        updated_receipt = ReceiptSchema().dump(receipt)
        session.close()
        return updated_receipt

    @staticmethod
    def delete(receipt_id: int) -> int:
        session = Session()
        session.query(Receipt).filter_by(id_r=receipt_id).delete()
        session.commit()
        session.close()

        return receipt_id

    @staticmethod
    def check_receipt_exists_by_id(receipt_id: int):
        existing_receipt = ReceiptDBService.get_receipt_by_id(receipt_id)
        if not existing_receipt:
            msg = {
                'code': 'RECEIPT_NOT_FOUND',
                'message': f'Receipt with id <{receipt_id}> does not exist.'
            }

            return msg

    @staticmethod
    def is_project_solde(id_receipt):
        session = None
        try:
            session = Session()
            receipt_project_object = session.query(Receipt.id_r) \
                .join(Funding, Funding.id_f == Receipt.id_f) \
                .join(Project, Project.id_p == Funding.id_p) \
                .add_columns(Project.statut_p) \
                .filter(Receipt.id_r == id_receipt).first()

            return len(receipt_project_object) > 1 and receipt_project_object[1] is True
        except:
            return False
        finally:
            session.close()
