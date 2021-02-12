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
    def get_receipts_of_year_by_funding_id(funding_id: int or str, year: int or str, receipt_id: int = None):
        session = None
        response = None
        try:
            session = Session()
            if receipt_id is not None:
                response = session.query(Receipt) \
                    .filter(Receipt.id_r != receipt_id, Receipt.id_f == funding_id, Receipt.annee_r == year) \
                    .first()
            else:
                response = session.query(Receipt) \
                    .filter(Receipt.id_f == funding_id, Receipt.annee_r == year) \
                    .first()
           
            if response is not None:
                msg = "L\'année {} de la recette de ce financement est déjà utilisé sur une recette.".format(year)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.DUPLICATION_VALUE_ERROR, msg, 409)
            return response
        except Exception as error:
            current_app.logger.error(f"ReceiptDBService - get_receipts_of_year_by_funding_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptDBService - get_receipts_of_year_by_funding_id : {error}")
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

            session = Session()
            receipts_object = session.query(*[c.label(c.name) for c in Receipt.__table__.c], (
                    Receipt.montant_r - func.coalesce(func.sum(Amount.montant_ma), 0)).label('difference')) \
                .join(Amount, Amount.id_r == Receipt.id_r, isouter=True) \
                .filter(Receipt.id_f == funding_id) \
                .group_by(Receipt.id_r) \
                .order_by(Receipt.id_r.desc()) \
                .all()

            receipts = []
            schema = ReceiptSchema(many=True)
            receipts = schema.dump(receipts_object)

            return receipts
        except Exception as error:
            current_app.logger.error(f"ReceiptDBService - get_receipts_by_funding_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptDBService - get_receipts_by_funding_id : {error}")
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
                msg = f'La recette n\'existe pas'
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)

            return receipt
        except Exception as error:
            current_app.logger.error(f"ReceiptDBService - get_receipt_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptDBService - get_receipt_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(receipt):
        session = None
        new_receipt = None
        try:
            
            posted_receipt = ReceiptSchema(only=('id_f', 'montant_r', 'annee_r')).load(receipt)
            receipt = Receipt(**posted_receipt)
            
            session = Session()
            session.add(receipt)
            session.commit()

            new_receipt = ReceiptSchema().dump(receipt)
            return new_receipt
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - insert : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(receipt):
        session = None
        updated_receipt = None
        try:
            data = ReceiptSchema(only=('id_r', 'id_f', 'montant_r', 'annee_r')).load(receipt)
            receipt = Receipt(**data)

            session = Session()
            session.merge(receipt)
            session.commit()

            updated_receipt = ReceiptSchema().dump(receipt)
            return updated_receipt
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - update : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def delete(receipt_id: int, year: int):
        session = None
        try:
            session = Session()
            delete_amounts = Amount.__table__.delete().where(Amount.id_r==receipt_id)
            session.execute(delete_amounts)
            
            data = session.query(Receipt).filter_by(id_r=receipt_id).delete()
            session.commit()

            return { 'message': 'La recette de l\'année {} a été supprimé'.format(year) }
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ReceiptDBService - delete : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def is_project_solde(id_receipt: int = None, funding_id: int = None):
        session = None
        try:
            session = Session()
            project = None
            if funding_id is not None:
                project = session.query(Project) \
                    .join(Funding, Project.id_p == Funding.id_p, isouter=True) \
                    .filter(Funding.id_f == funding_id, Project.statut_p == True) \
                    .first()
            elif id_receipt is not None:
                project = session.query(Project) \
                    .join(Funding, Project.id_p == Funding.id_p, isouter=True) \
                    .join(Receipt, Funding.id_f == Receipt.id_f, isouter=True) \
                    .filter(Receipt.id_r == id_receipt, Project.statut_p == True) \
                    .first()

            if project is not None and project.statut_p == True:
                msg = 'Le projet {} est soldé. Les actions dans le tableau des recettes relié à ce projet sont interdites.'.format(project.nom_p)
                ManageErrorUtils.value_error(CodeError.RECEIPT_PROJECT_CLOSED, TError.DELETE_ERROR, msg, 403)
        except Exception as error:
            current_app.logger.error(f"ReceiptDBService - is_project_solde : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptDBService - is_project_solde : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_sum_value(receipt, receipt_id: int = None): 
        session = None
        response = []
        try:
            session = Session()     
            diff = -1
            if receipt_id is None:
                # check insert
                response = session.query(Funding, \
                    ( Funding.montant_arrete_f - func.coalesce(func.sum(Receipt.montant_r), 0) ).label('difference') ) \
                    .join(Receipt, Receipt.id_f == Funding.id_f, isouter=True) \
                    .filter(Funding.id_f == receipt['id_f']) \
                    .group_by(Funding.id_f).all()
                diff = (0 if len(response) == 0 else float(response[0][1]))
            else:
                # check update
                response = session.query(Funding, \
                    ( Funding.montant_arrete_f - func.coalesce(func.sum(Receipt.montant_r), 0) ).label('difference') ) \
                    .join(Receipt, Receipt.id_f == Funding.id_f, isouter=True) \
                    .filter(Funding.id_f == receipt['id_f'], Receipt.id_r != receipt_id) \
                    .group_by(Funding.id_f).all()
                difference = (float(receipt['montant_r']) if len(response) == 0 else float(response[0][1]))
                diff = difference - float(receipt['montant_r'])
            
            if diff < 0:
                msg = "Erreur de valeur: la somme des recettes est supérieur au montant de son financement."
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, msg, 422)

            session.close()
        except Exception as error:
            current_app.logger.error(f"ReceiptDBService - check_sum_value : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ReceiptDBService - check_sum_value : {error}")
            raise
        finally:
            if session is not None:
                session.close()    
                  