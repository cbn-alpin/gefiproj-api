from flask import current_app

from src.shared.entity import Session
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
from .entities import InputOutput, InputOutputSchema


class InputOutputDBService:
    @staticmethod
    def check_input_output_exists(input_output_id):
        session = None
        try:
            session = Session()
            existing_input_output = session.query(InputOutput).filter_by(id_es=input_output_id).first()
            if existing_input_output is None:
                msg = "L'entrée sortie n'existe pas"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DATA_NOT_FOUND, msg, 404)
        except Exception as error:
            current_app.logger.error(f"InputOutputDBService - check_input_output_exists : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"InputOutputDBService - check_input_output_exists : {error}")
            raise
        finally:
            if session is not None:
                session.close()    

    @staticmethod
    def check_input_output_uniqueness(annee_recette, annee_affectation, input_output_id=None):
        session = None
        try:
            session = Session()
            existing_input_output = session.query(InputOutput).filter(InputOutput.annee_recette_es == annee_recette,
                                                                      InputOutput.annee_affectation_es == annee_affectation)
            if input_output_id is not None:
                existing_input_output = existing_input_output.filter(InputOutput.id_es != input_output_id)
            existing_input_output = existing_input_output.first()

            if existing_input_output is not None:
                msg = f'L\'entrée sortie ({annee_recette} , {annee_affectation}) existe déjà.'
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 400)
        except Exception as error:
            current_app.logger.error(f"InputOutputDBService - check_input_output_uniqueness : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"InputOutputDBService - check_input_output_uniqueness : {error}")
            raise
        finally:
            if session is not None:
                session.close()    

    @staticmethod
    def get_input_output_by_id(input_output_id: int):
        session = None
        try:
            session = Session()
            input_output_object = session.query(InputOutput).filter_by(id_es=input_output_id).first()

            schema = InputOutputSchema()
            input_output = schema.dump(input_output_object)

            if input_output is None:
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_WARNING, TError.DATA_NOT_FOUND,
                                             'Cette entrée sortie n\'existe pas', 404)

            return input_output
        except Exception as error:
            current_app.logger.error(f"InputOutputDBService - get_input_output_by_id : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"InputOutputDBService - get_input_output_by_id : {error}")
            raise
        finally:
            if session is not None:
                session.close()    

    @staticmethod
    def get_input_output_by_filter(query_param=None):
        session = None
        try:
            session = Session()
            input_outputs = session.query(InputOutput)

            if query_param is not None:
                annee_recette_es = query_param.get('annee_recette_es', default=None, type=int)
                if annee_recette_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es == annee_recette_es)

                annee_recette_es_sup = query_param.get('annee_recette_es_sup', default=None, type=int)
                if annee_recette_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es >= annee_recette_es_sup)

                annee_recette_es_inf = query_param.get('annee_recette_es_inf', default=None, type=int)
                if annee_recette_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es <= annee_recette_es_inf)

                annee_affectation_es = query_param.get('annee_affectation_es', default=None, type=int)
                if annee_affectation_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es == annee_affectation_es)

                annee_affectation_es_sup = query_param.get('annee_affectation_es_sup', default=None, type=int)
                if annee_affectation_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es >= annee_affectation_es_sup)

                annee_affectation_es_inf = query_param.get('annee_affectation_es_inf', default=None, type=int)
                if annee_affectation_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es <= annee_affectation_es_inf)

                montant_es = query_param.get('montant_es', default=None, type=float)
                if montant_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es == montant_es)

                montant_es_sup = query_param.get('montant_es_sup', default=None, type=float)
                if montant_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es >= montant_es_sup)

                montant_es_inf = query_param.get('montant_es_inf', default=None, type=float)
                if montant_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es <= montant_es_inf)
            input_outputs = input_outputs.all()
            input_outputs = InputOutputSchema(many=True).dump(input_outputs)
            if input_outputs is None:
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_WARNING, TError.DATA_NOT_FOUND,
                                             'Cette-es entrée-s sortie-s n\'existe-nt pas', 404)
            else:
                if len(input_outputs) == 0:
                    ManageErrorUtils.value_error(CodeError.DB_VALIDATION_WARNING, TError.DATA_NOT_FOUND,
                                                 'Il n\'y a pas d\'entrée sorties satisfaisants vos critères', 404)

            return input_outputs
        except Exception as error:
            current_app.logger.error(f"InputOutputDBService - get_input_output_by_filter : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"InputOutputDBService - get_input_output_by_filter : {error}")
            raise
        finally:
            if session is not None:
                session.close()    

    @staticmethod
    def insert(input_output: InputOutput):
        session = None
        inserted_input_output = None
        try:
            session = Session()
            session.add(input_output)
            if input_output is None:
                msg = "Une erreur est survenue lors de l'enregistrement de cette entrée sortie"
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_WARNING, TError.INSERT_ERROR, msg, 500)
            else:
                session.commit()
                inserted_input_output = InputOutputSchema().dump(input_output)
            return inserted_input_output
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - insert : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - insert : {error}")
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(input_output: InputOutput):
        session = None
        try:
            session = Session()
            session.merge(input_output)
            session.commit()

            updated_input_output = InputOutputSchema().dump(input_output)
            return updated_input_output
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - update : {error}")
            raise
        finally:
            if session is not None:
                session.close()
                
    @staticmethod
    def delete(input_output_id: int) -> int:
        session = None
        try:
            session = Session()
            session.query(InputOutput).filter_by(id_es=input_output_id).delete()
            session.commit()

            return input_output_id
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"InputOutputDBService - delete : {error}")
            raise
        finally:
            if session is not None:
                session.close()
