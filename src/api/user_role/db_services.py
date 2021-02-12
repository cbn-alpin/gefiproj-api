from src.shared.entity import Session
from ..user_role.entities import UserRole, UserRoleSchema
from src.shared.manage_error import ManageErrorUtils, CodeError, TError
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
                
                # Return created data
                response = UserRoleSchema().dump(data)
                session.close()
                
            return response
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - insert_user_role : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - insert_user_role : {error}")
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
                
                response = UserRoleSchema().dump(data)
                session.close()
            return response
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - update_user_role : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - update_user_role : {error}")
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
            
            session.close()
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - delete_user_role : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"UserRoleDBService - delete_user_role : {error}")
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
        except Exception as error:
            current_app.logger.error(f"UserRoleDBService - get_user_role : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"UserRoleDBService - get_user_role : {error}")
            raise
        finally:
            if session is not None:
                session.close()
