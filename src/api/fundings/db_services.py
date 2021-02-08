from flask import current_app
from enum import Enum 
from src.shared.manage_error import CodeError, ManageErrorUtils, TError
from sqlalchemy import func, case
from marshmallow import INCLUDE, EXCLUDE
from src.shared.entity import Session

from .entities import Funding, FundingSchema
from ..amounts.entities import Amount
from ..receipts.entities import Receipt, ReceiptSchema
from ..users.db_services import UserDBService
from src.api.funders.entities import Funder
from datetime import datetime


class Status(Enum):
    STATUS_DEFAULT = 'ANTR'
    STATUS_SOLDE = 'SOLDE'
    

class FundingDBService:
    @staticmethod
    def get_fundings_by_project(project_id: int):
        session = None
        response = []
        try:
            session = Session()
            # if statut_f is solde return True else False
            expr = case([ (Funding.statut_f == Status.STATUS_SOLDE.value, True) ], \
                        else_ = False)
            # get all fundings referenced by project, check if is solde and the difference between montant_arrete_f and the sum of receipts reference by his funding
            fundings = session.query(*[c.label(c.name) for c in Funding.__table__.c], expr.label('solde'), \
                *[c.label(c.name) for c in Funder.__table__.c], \
                ( Funding.montant_arrete_f - func.coalesce(func.sum(Receipt.montant_r), 0) ).label('difference')) \
                .join(Funder, Funding.id_financeur == Funder.id_financeur) \
                .join(Receipt, Receipt.id_f == Funding.id_f, isouter=True) \
                .filter(Funding.id_p == project_id) \
                .group_by(Funding.id_f, Funder.id_financeur) \
                .order_by(Funding.id_f.desc()) \
                .all()
                
            schema = FundingSchema(many=True, unknown=INCLUDE)
            response = schema.dump(fundings)
                
            for f in response:
                f['financeur'] = {}
                f['financeur']['id_financeur'] = f['id_financeur']
                if 'nom_financeur' in f:
                    f['financeur']['nom_financeur'] = f['nom_financeur']
                    del f['nom_financeur']
                if 'ref_arret_attributif_financeur' in f:
                    f['financeur']['ref_arret_attributif_financeur'] = f['ref_arret_attributif_financeur']
                    del f['ref_arret_attributif_financeur']
                
            session.close()
            return response
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_project_not_have_funding(project_id: int):
        session = None
        response = None
        try:
            session = Session()
            response = session.query(Funding).filter_by(id_p=project_id).first()
            if response is not None:
                ManageErrorUtils.value_error(CodeError.DB_VALUE_REFERENCED, TError.DELETE_ERROR, 'Le projet est réferencé à un ou plusieurs financements', 403)
        
            session.close()
            return response
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_funding_by_funder(funder_id: int):
        session = None
        response = None
        try:
            session = Session()  
            funding_object = session.query(Funding).filter_by(id_financeur=funder_id) \
                .order_by(Funding.id_f.desc()) \
                .all()

            # Transforming into JSON-serializable objects
            schema = FundingSchema(many=True)
            response = schema.dump(funding_object)
            
            # Serializing as JSON
            session.close()
            return response
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(funding):
        session = None
        new_funding = None
        try:
            posted_funding = FundingSchema(only=(
                'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f', 'date_limite_solde_f',
                'commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f', 'imputation_f')) \
                .load(funding, unknown=EXCLUDE)
            funding = Funding(**posted_funding)

            # Persist funding
            session = Session()
            session.add(funding)
            session.commit()
            
            if funding is None:
                msg = "Une erreur est survenue lors de l'enregistrement du financement"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.INSERT_ERROR, msg, 404)
            
            # Return created funding
            new_funding = FundingSchema().dump(funding)
            session.close()
            return new_funding
        except ValueError as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(funding):
        session = None
        updated_funding = None
        try:
            # Mount funding object
            funding = FundingSchema(only=(
                'id_f', 'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f',
                'date_limite_solde_f', 'commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f',
                'imputation_f')) \
                .load(funding, unknown=EXCLUDE)
            funding = Funding(**funding)
            # Start DB session
            session = Session()
            session.merge(funding)
            session.commit()

            # Return updated funding
            updated_funding = FundingSchema().dump(funding)
            session.close()
            return updated_funding
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()       

    @staticmethod
    def can_update(project_id: int):
        try:
            if UserDBService.is_responsable_of_projet(project_id) == False and UserDBService.is_admin() == False:
                msg = 'Ce financement ne peut pas être modifier car vous n\'êtes ni administrateur ni responsable du projet.'
                ManageErrorUtils.exception(CodeError.NOT_PERMISSION, TError.UPDATE_ERROR, msg, 403)
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        
    @staticmethod
    def get_funding_by_id(funding_id: int):
        session = None
        funding = None
        try:
            session = Session()
            funding = session.query(Funding).filter_by(id_f=funding_id).first()

            if funding is None:
                msg = 'Le financement \'{funding_id}\' n\'existe pas.'.format(funding_id)
                ManageErrorUtils.exception(CodeError.NOT_PERMISSION, TError.UPDATE_ERROR, msg, 404)
            
            session.close()
            return funding
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()     

    @staticmethod
    def delete(funding_id: int):
        session = None
        try:
            session = Session()
            session.query(Funding).filter_by(id_f=funding_id).delete()
            session.commit()
            session.close()
            return {'message': f'Le financement \'{funding_id}\' a été supprimé'.format(funding_id)}
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()       

    @staticmethod
    def delete_entities_referenced(funding_id: int):
        session = None
        try:
            session = Session()
            receipts_object = session.query(Receipt).filter_by(id_f=funding_id).all()
            schema = ReceiptSchema(many=True)
            receipts = schema.dump(receipts_object)
            for r in receipts:
                delete_amounts = Amount.__table__.delete().where(Amount.id_r==r['id_r'])
                session.execute(delete_amounts)
                delete_receipt = Receipt.__table__.delete().where(Receipt.id_r==r['id_r'])
                session.execute(delete_receipt)
                
            session.commit()
            session.close()
        except (Exception, ValueError) as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()       

    @staticmethod
    def convert_funding_dates(funding):
        if 'date_solde_f' in funding and funding['date_solde_f'] is not None:
            funding['date_solde_f'] = FundingDBService.date_convert(funding['date_solde_f'])
        if 'date_arrete_f' in funding and funding['date_solde_f'] is not None:
            funding['date_arrete_f'] = FundingDBService.date_convert(funding['date_arrete_f'])
        if 'date_limite_solde_f' in funding and funding['date_solde_f'] is not None:
            funding['date_limite_solde_f'] = FundingDBService.date_convert(funding['date_limite_solde_f'])
        return funding
    
    @staticmethod
    def date_convert(date_time_str):
        date = None
        date_time_obj = date_time_str.strftime('%Y-%m-%d')
        return date_time_obj
    