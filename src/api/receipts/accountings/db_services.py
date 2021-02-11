from flask import current_app

from src.shared.entity import Session
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
from .entities import ReceiptAccounting, ReceiptAccountingSchema


class ReceiptAccountingDBService:
    @staticmethod
    def get_receipts_accountings():
        session = None
        try:
            session = Session()
            receipts_accountings_object = session.query(ReceiptAccounting).all()

            schema = ReceiptAccountingSchema(many=True)
            receipts_accountings = schema.dump(receipts_accountings_object)
            return receipts_accountings
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(receipt_accounting):
        session = None
        try:

            posted_receipt_accounting = ReceiptAccountingSchema(only=('id_rc', 'montant_rc', 'annee_rc')).load(
                receipt_accounting)
            data = ReceiptAccounting(**posted_receipt_accounting)

            session = Session()
            session.add(data)
            session.commit()

            inserted_amount = ReceiptAccountingSchema().dump(data)
            return inserted_amount
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(receipt_accounting):
        session = None
        try:
            update_receipt_accounting = ReceiptAccountingSchema(only=('id_rc', 'montant_rc', 'annee_rc')).load(
                receipt_accounting)
            data = ReceiptAccounting(**update_receipt_accounting)

            session = Session()
            session.merge(data)
            session.commit()

            update_expense = ReceiptAccountingSchema().dump(data)
            session.close()
            return update_receipt_accounting
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def delete(receipt_accounting_id: int):
        session = None
        try:
            session = Session()
            receipt_accounting = session.query(ReceiptAccounting).filter_by(id_rc=receipt_accounting_id).first()
            session.delete(receipt_accounting)
            session.commit()
            response = {
                'message': f'La recette comptable de l\'année {receipt_accounting.annee_rc} a été supprimé.'
            }
            return response
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_unique_year(year: int, receipt_accounting_id=None):
        session = None
        try:
            session = Session()
            if receipt_accounting_id is not None:
                receipt_accounting_existing = session.query(ReceiptAccounting).filter(
                    ReceiptAccounting.id_rc != receipt_accounting_id, ReceiptAccounting.annee_rc == year).first()
            else:
                receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(annee_rc=year).first()
            session.close()

            if receipt_accounting_existing is not None:
                msg = f'La recette comptable de l\'année {year} existe déjà.'
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 403)
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_exist_receipt_accounting(receipt_accounting_id: int):
        session = None
        try:
            session = Session()
            receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(
                id_rc=receipt_accounting_id).first()

            if receipt_accounting_existing is None:
                msg = f'La recette comptable n\'existe pas.'
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

        session = Session()
        receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(id_rc=receipt_accounting_id).first()

        if receipt_accounting_existing is None:
            raise ValueError(f'La recette comptable n\'existe pas.', 404)
