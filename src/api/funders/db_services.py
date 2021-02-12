from flask import current_app
from src.shared.entity import Session
from .entities import Funder, FunderSchema
from ..fundings.entities import Funding
from src.shared.manage_error import CodeError, ManageErrorUtils, TError


class FunderDBService:
    @staticmethod
    def get_all_funders():
        session = None
        response = []
        try:
            session = Session()  
            funders_object = session.query(Funder).order_by(Funder.nom_financeur).all()
            # Transforming into JSON-serializable objects
            schema = FunderSchema(many=True)
            response = schema.dump(funders_object)
            
            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"FunderDBService - get_all_funders : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FunderDBService - get_all_funders : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_funder_by_id(funder_id: int):
        session = None
        response = None
        try:
            session = Session()  
            funder = session.query(Funder).filter_by(id_financeur=funder_id).first()
        
            if funder is None:
                msg = "Le financeur n'existe pas"
                ManageErrorUtils.value_error(CodeError.DB_VALUE_REFERENCED, TError.DATA_NOT_FOUND, msg, 404)
            
            schema = FunderSchema()
            response = schema.dump(funder)
            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"FunderDBService - get_funder_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FunderDBService - get_funder_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def check_unique_funder_name(name: str, funder_id:int = None):
        session = None
        response = None
        try:
            session = Session()  
            if funder_id is not None:
                response = session.query(Funder) \
                    .filter(Funder.id_financeur != funder_id, Funder.nom_financeur == name) \
                    .first()
            else:
                response = session.query(Funder).filter_by(nom_financeur=name).first()
            
            if response is not None:
                msg = "Le nom du financeur '{} est déjà utilisé sur un autre financeur".format(name)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 409)

            session.close()
            return response
        except Exception as error:
            current_app.logger.error(f"FunderDBService - check_unique_funder_name : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FunderDBService - check_unique_funder_name : {error}")
            raise
        finally:
            if session is not None:
                session.close()      
            
    @staticmethod
    def insert(funder):
        session = None
        new_funder = None
        try:
            posted_funder = FunderSchema(only=('nom_financeur', 'ref_arret_attributif_financeur')).load(funder)
            funder = Funder(**posted_funder)
        
            session = Session()
            session.add(funder)
            session.commit()
            
            new_funder = FunderSchema().dump(funder)
            session.close()
            return new_funder
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - insert : {error}")
            raise
        finally:
            if session is not None:
                session.close()
        
    @staticmethod
    def update(funder):
        session = None
        update_funder = None
        try:
            data = FunderSchema(only=('id_financeur', 'nom_financeur', 'ref_arret_attributif_financeur')).load(funder)
            funder = Funder(**data)
        
            session = Session()
            session.merge(funder)
            session.commit()
            
            update_funder = FunderSchema().dump(funder)
            session.close()
            return update_funder
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - update : {error}")
            raise
        finally:
            if session is not None:
                session.close()            
    
    @staticmethod
    def delete(funder_id: int, nom: str):
        session = None
        try:
            session = Session()
            data = session.query(Funder).filter_by(id_financeur=funder_id).delete()
            session.commit()
            
            session.close()
            return { 'message': 'Le financeur \'{}\' a été supprimé'.format(nom) }
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"FunderDBService - delete : {error}")
            raise
        finally:
            if session is not None:
                session.close()
                
    @staticmethod
    def check_funder_referenced_in_funding(funder_id: int, name: str):
        session = None
        try:
            session = Session() 
            fundings = [] 
            fundings = session.query(Funder) \
                .join(Funding, Funder.id_financeur == Funding.id_financeur) \
                .filter(Funder.id_financeur == funder_id) \
                .all()
                
            if fundings is not None and len(fundings) > 0:
                msg = "Le financeur '{}' est affecté à un ou plusieurs financements".format(name)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.DELETE_ERROR, msg, 404)

            session.close()
        except Exception as error:
            current_app.logger.error(f"FunderDBService - check_funder_referenced_in_funding : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"FunderDBService - check_funder_referenced_in_funding : {error}")
            raise
        finally:
            if session is not None:
                session.close()
