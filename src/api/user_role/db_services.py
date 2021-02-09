from src.shared.entity import Session
from ..user_role.entities import UserRole, UserRoleSchema
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
import sqlalchemy
from flask import current_app


class UserRoleDBService:
    @staticmethod
    def insert_user_role(id_u: int, id_ra: int):
        session = None
        response = None
        try:
            user_role = UserRoleDBService.get_user_role(id_u, id_ra)
            if user_role is None:
                user_role = { 'id_u': id_u, 'id_ra': id_ra }
                schema = UserRoleSchema(only=('id_u','id_ra')).load(user_role)
                data = UserRole(**schema)

                session = Session()
                session.add(data)
                session.commit()
                
                if data is None:                
                    msg = "Une erreur est survenue lors de l'insertion d'un rôle à un utilisateur"
                    ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.INSERT_ERROR, msg, 404)
           
                # Return created data
                response = UserRoleSchema().dump(data)
                session.close()
                
            return response
        except (Exception, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            session.rollback()
            current_app.logger.error(e)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def update_user_role(id_u: int, id_ra: int):
        session = None
        response = None
        try:
            user_role = UserRoleDBService.get_user_role(id_u, id_ra)
            if user_role is None:
                user_role = { 'id_u': id_u, 'id_ra': id_ra}
                schema = UserRoleSchema(only=('id_u','id_ra')).load(user_role)
                data = UserRole(**schema)

                session = Session()
                session.merge(data)
                session.commit()
                
                if data is None:                
                    msg = "Une erreur est survenue lors de la modification du rôle d'un utilisateur"
                    ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.UPDATE_ERROR, msg, 404)
                
                response = UserRoleSchema().dump(data)
                session.close()
            return response
        except (Exception, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            session.rollback()
            current_app.logger.error(e)
            raise
        finally:
            if session is not None:
                session.close()
                
    @staticmethod
    def delete_user_role(id_u: int, id_ra: int):
        session = None
        try:
            session = Session()
            data = session.query(UserRole) \
                .filter(UserRole.id_u == id_u, UserRole.id_ra == id_ra) \
                .delete()
            session.commit()
            
            if data is None:                
                msg = "Une erreur est survenue lors de la suppression du rôle d'un utilisateur"
                ManageErrorUtils.exception(CodeError.DB_VALIDATION_ERROR, TError.DELETE_ERROR, msg, 404)
                
            session.close()
        except (Exception, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            session.rollback()
            current_app.logger.error(e)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_user_role(id_u: int, id_ra: int):
        session = None
        response = None
        try:
            session = Session()
            user_role_object = session.query(UserRole) \
                .filter(UserRole.id_u == id_u, UserRole.id_ra == id_ra) \
                .first()
            session.close()
            
            if user_role_object is not None:
                schema = UserRoleSchema(only=('id_u','id_ra'))
                response = schema.dump(user_role_object)
                
            return response
        except (Exception, sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            current_app.logger.error(e)
            raise
        finally:
            if session is not None:
                session.close()
