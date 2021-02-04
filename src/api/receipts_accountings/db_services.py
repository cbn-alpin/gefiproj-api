from src.shared.entity import Session
from .entities import ReceiptAccounting, ReceiptAccountingSchema
from sqlalchemy import func


class ReceiptAccountingDBService:
    @staticmethod
    def get_receipts_accountings():
        session = Session()
        receipts_accountings_object = session.query(ReceiptAccounting).all()
        
        schema = ReceiptAccountingSchema(many=True)
        receipts_accountings = schema.dump(receipts_accountings_object)
        session.close()
        return receipts_accountings


    @staticmethod
    def insert(receipt_accounting):
        posted_receipt_accounting = ReceiptAccountingSchema(only=('id_rc', 'montant_rc', 'annee_rc')).load(receipt_accounting)
        data = ReceiptAccounting(**posted_receipt_accounting)
        
        session = Session()
        session.add(data)
        session.commit()

        inserted_amount = ReceiptAccountingSchema().dump(data)
        session.close()
        return inserted_amount

    @staticmethod
    def update(receipt_accounting):
        update_receipt_accounting = ReceiptAccountingSchema(only=('id_rc', 'montant_rc', 'annee_rc')).load(receipt_accounting)
        data = ReceiptAccounting(**update_receipt_accounting)
        
        session = Session()
        session.merge(data)
        session.commit()

        update_expense = ReceiptAccountingSchema().dump(data)
        session.close()
        return update_receipt_accounting
    
    @staticmethod
    def delete(receipt_accounting_id: int):
        session = Session()
        receipt_accounting = session.query(ReceiptAccounting).filter_by(id_rc=receipt_accounting_id).first()
        session.delete(receipt_accounting)
        session.commit()
        session.close()
        response = {
            'message': f'La recette comptable de l\'année {receipt_accounting.annee_rc} a été supprimé.'
        }
        return response
    
    @staticmethod
    def check_unique_year(year: int, receipt_accounting_id = None):
        session = Session()  
        if receipt_accounting_id is not None:
            receipt_accounting_existing = session.query(ReceiptAccounting).filter(ReceiptAccounting.id_rc != receipt_accounting_id, ReceiptAccounting.annee_rc == year).first()
        else:
            receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(annee_rc=year).first()
        session.close()
        
        if receipt_accounting_existing is not None:
            raise ValueError(f'La recette comptable de l\'année {year} existe déjà.',403)
        
    @staticmethod
    def check_exist_receipt_accounting(receipt_accounting_id: int):
        session = Session()  
        receipt_accounting_existing = session.query(ReceiptAccounting).filter_by(id_rc=receipt_accounting_id).first()
        session.close()
        
        if receipt_accounting_existing is None:
            raise ValueError(f'La recette comptable n\'existe pas.',404)
   