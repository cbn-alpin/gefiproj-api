from flask import current_app

from src.shared.entity import Session
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
from .entities import ReceiptAccounting, ReceiptAccountingSchema


class ReceiptAccountingDBService:
    @staticmethod
    def get_receipts_accountings():
        session = None
        response = []
        try:
            session = Session()
            receipts_accountings_object = session.query(ReceiptAccounting).all()

            schema = ReceiptAccountingSchema(many=True)
            response = schema.dump(receipts_accountings_object)
            return response
        except Exception as error:
            current_app.logger.error(f"ReceiptAccountingDBService - get_receipts_accountings : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptAccountingDBService - get_receipts_accountings : {error}")
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
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - insert : {error}")
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
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - update : {error}")
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
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptAccountingDBService - delete : {error}")
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
                receipt_accounting_existing = session.query(ReceiptAccounting) \
                    .filter(ReceiptAccounting.id_rc != receipt_accounting_id, ReceiptAccounting.annee_rc == year).first()
            else:
                receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(annee_rc=year).first()
            session.close()

            if receipt_accounting_existing is not None:
                msg = 'La recette comptable de l\'année {} existe déjà.'.format(year)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 403)
        except Exception as error:
            current_app.logger.error(f"ReceiptAccountingDBService - check_unique_year : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptAccountingDBService - check_unique_year : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_receipt_accounting_by_id(receipt_accounting_id: int):
        session = None
        response = None
        try:
            session = Session()
            receipt_accounting_existing = session.query(ReceiptAccounting) \
                .filter_by(id_rc=receipt_accounting_id).first()

            if receipt_accounting_existing is None:
                msg = f'La recette comptable n\'existe pas.'
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)
            
            schema = ReceiptAccountingSchema()
            response = schema.dump(receipt_accounting_existing)
            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"ReceiptAccountingDBService - get_receipt_accounting_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptAccountingDBService - get_receipt_accounting_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()
