from enum import Enum

from flask import current_app
from marshmallow import INCLUDE, EXCLUDE
from sqlalchemy import func, case

from src.api.funders.entities import Funder
from src.shared.entity import Session
from src.shared.manage_error import CodeError, ManageErrorUtils, TError
from .entities import Funding, FundingSchema
from src.api.projects.entities import Project
from ..amounts.entities import Amount
from ..receipts.entities import Receipt, ReceiptSchema
from ..users.db_services import UserDBService


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
        except Exception as error:
            current_app.logger.error(f"FundingDBService - get_fundings_by_project : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - get_fundings_by_project : {error}")
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
        except Exception as error:
            current_app.logger.error(f"FundingDBService - check_project_not_have_funding : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - check_project_not_have_funding : {error}")
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
        except Exception as error:
            current_app.logger.error(f"FundingDBService - get_funding_by_funder : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - get_funding_by_funder : {error}")
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
            
            # Return created funding
            new_funding = FundingSchema().dump(funding)
            session.close()
            return new_funding
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - insert : {error}")
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
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - update : {error}")
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
        except Exception as error:
            current_app.logger.error(f"FundingDBService - can_update : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - can_update : {error}")
            raise
        
    @staticmethod
    def get_funding_by_id(funding_id: int):
        session = None
        try:
            session = Session()
            funding = session.query(Funding).filter_by(id_f=funding_id).first()

            if funding is None:
                msg = f'Le financement {funding_id} n\'existe pas.'
                ManageErrorUtils.value_error(CodeError.NOT_PERMISSION, TError.UPDATE_ERROR, msg, 404)
            
            session.close()
            return funding
        except Exception as error:
            current_app.logger.error(f"FundingDBService - get_funding_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - get_funding_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()     

    @staticmethod
    def delete(funding_id: int):
        session = None
        try:
            session = Session()
            data = session.query(Funding).filter_by(id_f=funding_id).delete()
            session.commit()
            
            session.close()
            return {'message': f'Le financement \'{funding_id}\' a été supprimé'.format(funding_id)}
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - delete : {error}")
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
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - delete_entities_referenced : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FundingDBService - delete_entities_referenced : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def check_sum_with_receipt(funding):
        session = None
        try:
            session = Session()
            sum_receipts = session.query( Funding.montant_arrete_f, \
                (func.coalesce(func.sum(Receipt.montant_r), 0)).label('sum')) \
                .join(Receipt, Receipt.id_f == Funding.id_f, isouter=True) \
                .filter(Funding.id_f == funding['id_f']) \
                .group_by(Funding.id_f) \
                .all()
            sum_receipts = ( 0 if len(sum_receipts) == 0 else float(sum_receipts[0][1]) )
            diff = float(funding['montant_arrete_f']) - sum_receipts
                
            if diff < 0:
                msg = "Erreur de valeur: la somme des montants des recettes est supérieur au montant arrêté du financement modifié."
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, msg, 422)

            session.close()
        except Exception as error:
            current_app.logger.error(f"FundingDBService - check_sum_with_receipt : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - check_sum_with_receipt : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def is_project_solde(funding_id: int = None, project_id: int = None):
        session = None
        try:
            session = Session()
            project = None
            if funding_id is not None:
                project = session.query(Project) \
                    .join(Funding, Project.id_p == Funding.id_p, isouter=True) \
                    .filter(Funding.id_f == funding_id, Project.statut_p == True) \
                    .first()
            elif project_id is not None:
                project = session.query(Project) \
                    .filter(Project.id_p == project_id, Project.statut_p == True) \
                    .first()
                
            if project is not None and project.statut_p == True:
                msg = "Le projet {} est soldé. Les actions dans le tableau des financements relié à ce projet sont interdites.".format(project.nom_p)
                ManageErrorUtils.value_error(CodeError.NOT_PERMISSION, TError.STATUS_SOLDE, msg, 403)
      
            session.close()
        except Exception as error:
            current_app.logger.error(f"FundingDBService - is_project_solde : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - is_project_solde : {error}")
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def check_fundings_not_solde_by_project(project_id: int, name: str):
        session = None
        try:
            session = Session()
            fundings = []
            fundings = session.query(Funding) \
                .filter(Funding.id_p == project_id, Funding.statut_f == Status.STATUS_SOLDE.value) \
                .all()
            
            if fundings is not None or len(fundings) > 0:
                msg = "Le projet {} ne peut pas soldé car celui-ci possède {} financements non soldé.".format(name, len(fundings))
                ManageErrorUtils.value_error(CodeError.NOT_PERMISSION, TError.STATUS_SOLDE, msg, 403)
      
            session.close()
        except Exception as error:
            current_app.logger.error(f"FundingDBService - check_fundings_not_solde_by_project : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FundingDBService - check_fundings_not_solde_by_project : {error}")
            raise
        finally:
            if session is not None:
                session.close()