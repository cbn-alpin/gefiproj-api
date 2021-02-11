from flask import current_app
from sqlalchemy import func

from src.shared.entity import Session
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
from .entities import Receipt, ReceiptSchema
from ..amounts.entities import Amount
from ..fundings.entities import Funding
from ..projects.entities import Project


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = None
        try:
            session = Session()
            existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()

            if existing_funding is None:
                msg = "Le finnacement n\'existe pas."
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_receipts_of_year_by_funding_id(funding_id: int or str, year: int or str):
        session = None
        try:
            session = Session()
            receipts = session.query(Receipt).filter(Receipt.id_f == funding_id, Receipt.annee_r == year).all()
            receipts = ReceiptSchema(many=True).dump(receipts)
            if len(receipts) > 0:
                msg = f"Le financement {funding_id} a déjà une recette pour l'année {year}."
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DUPLICATION_VALUE_ERROR, msg, 400)
            return receipts
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_receipts_by_funding_id(funding_id: int):
        session = None
        try:
            session = Session()
            receipt_object = session.query(Receipt).filter_by(id_f=funding_id).order_by(Receipt.id_r).all()

            rest_receipt_amount_object = session.query(*[c.label(c.name) for c in Receipt.__table__.c], (
                    Receipt.montant_r - func.coalesce(func.sum(Amount.montant_ma), 0)).label('difference')) \
                .join(Amount, Amount.id_r == Receipt.id_r, isouter=True) \
                .filter(Receipt.id_f == funding_id) \
                .group_by(Receipt.id_r) \
                .order_by(Receipt.id_r.desc()) \
                .all()

            receipts = []
            for r in rest_receipt_amount_object:
                receipts.append(r._asdict())

            return receipts
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_receipt_by_id(receipt_id: int):
        session = None
        try:
            session = Session()
            receipt_object = session.query(Receipt).filter_by(id_r=receipt_id).first()

            schema = ReceiptSchema()
            receipt = schema.dump(receipt_object)

            if not receipt:
                msg = f'La recette avec id =  {receipt_id} n\'existe pas'
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)

            return receipt
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(receipt: Receipt):
        session = None
        try:
            session = Session()
            session.add(receipt)
            session.commit()

            inserted_receipt = ReceiptSchema().dump(receipt)
            return inserted_receipt
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(receipt: Receipt):
        session = None
        try:
            session = Session()
            session.merge(receipt)
            session.commit()

            updated_receipt = ReceiptSchema().dump(receipt)
            return updated_receipt
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def delete(receipt_id: int) -> int:
        try:
            session = Session()
            session.query(Receipt).filter_by(id_r=receipt_id).delete()
            session.commit()

            return receipt_id
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_receipt_exists_by_id(receipt_id: int):
        existing_receipt = ReceiptDBService.get_receipt_by_id(receipt_id)
        if not existing_receipt:
            msg = {
                'code': 'RECEIPT_NOT_FOUND',
                'message': f'Recette avec id = <{receipt_id}> n\'existe pas.'
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

            if len(receipt_project_object) > 1 and receipt_project_object[1] is True:
                msg = f'La recette avec  {id_receipt} ne peut pas être supprimée. Le projet associé est fermé.'
                ManageErrorUtils.exception(CodeError.RECEIPT_PROJECT_CLOSED, TError.DELETE_ERROR, msg, 400)

        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
