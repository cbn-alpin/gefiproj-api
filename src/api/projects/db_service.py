from flask import current_app
from sqlalchemy.orm import subqueryload
from sqlalchemy import or_
from marshmallow import EXCLUDE

from src.shared.entity import Session
from .entities import Project, ProjectSchema
from src.shared.manage_error import CodeError, ManageErrorUtils, TError
from enum import Enum

class Status(Enum):
    STATUS_DEFAULT = False
    STATUS_SOLDE = True
    

class ProjectDBService:
    @staticmethod
    def check_unique_code_and_name(code_p: str, nom_p: str, project_id: int = None):
        session = None
        response = None
        try:
            session = Session()
            project = {}
            if project_id is not None:
                project = session.query(Project) \
                    .filter(Project.id_p != project_id) \
                    .filter(or_(Project.code_p == code_p, Project.nom_p == nom_p)) \
                    .first()
            else:
                project = session.query(Project) \
                    .filter(or_(Project.code_p == code_p, Project.nom_p == nom_p)) \
                    .first()
                    
            session.close()
            if project is not None:
                msg = "Le code projet '{}' ou le nom du projet '{} sont déjà utilisés sur un autre projet".format(code_p, nom_p)
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_ERROR, TError.UNIQUE_CONSTRAINT_ERROR, msg, 409)

            return project
        except Exception as error:
            current_app.logger.error(error)
            raise
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(project):
        session = None
        new_project = None
        try:
            posted_project = ProjectSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u')).load(project, unknown=EXCLUDE)
            project = Project(**posted_project)
            
            # Start DB session
            session = Session()
            session.add(project)
            session.commit()
    
            new_project = ProjectSchema().dump(project)
            session.close()
            return new_project
        except Exception as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_all_projects():
        session = None
        projects = []
        try:
            session = Session()
            projects_objects = session.query(Project) \
                .options(subqueryload(Project.responsable))

            # Transforming into JSON-serializable objects
            schema = ProjectSchema(many=True, exclude=['id_u'])
            projects = schema.dump(projects_objects)

            # Serializing as JSON
            session.close()
            return projects
        except Exception as error:
            current_app.logger.error(error)
            raise
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_project_by_id(project_id: int, is_solde: bool = None):
        session = None
        project = None
        try:
            session = Session()
            project_object = session.query(Project) \
                .options(subqueryload(Project.responsable)) \
                .filter_by(id_p=project_id) \
                .first()

            if project_object is None:
                ManageErrorUtils.value_error(CodeError.DB_VALIDATION_WARNING, TError.DATA_NOT_FOUND, 'Le projet n\'existe pas', 404)
            if is_solde == True and project_object is not None and project_object.statut_p == True:
                msg = "Le projet {} est soldé. Les modifications sur ce projet sont interdites.".format(project_object.nom_p)
                ManageErrorUtils.value_error(CodeError.NOT_PERMISSION, TError.STATUS_SOLDE, msg, 403)
      
            # Transforming into JSON-serializable objects
            schema = ProjectSchema(exclude=['id_u'])
            project = schema.dump(project_object)
            session.close()
            return project
        except Exception as error:
            current_app.logger.error(error)
            raise
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def update(project):
        session = None
        update_project = None
        try:
            data = ProjectSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u', 'id_p')) \
                .load(project, unknown=EXCLUDE)
            project = Project(**data)
        
            session = Session()
            session.merge(project)
            session.commit()
            
            update_project = ProjectSchema().dump(project)
            session.close()
            return update_project   
        except Exception as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()             

    @staticmethod
    def delete(project_id: int, nom_p: str):
        session = None
        try:
            session = Session()
            data = session.query(Project).filter_by(id_p=project_id).delete()
            session.commit()
            
            session.close()
            return {'message': 'Le projet \'{}\' a été supprimé'.format(nom_p)}
        except Exception as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()    
   