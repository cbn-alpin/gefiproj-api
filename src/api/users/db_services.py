from enum import Enum
import numpy as np
from flask import current_app
from flask_jwt_extended import get_jwt_identity

from src.shared.entity import Session
from sqlalchemy import or_
from .entities import User, UserSchema, RevokedToken, RevokedTokenSchema
from ..projects.db_service import ProjectDBService
from ..role_acces.entities import RoleAccess, RoleAccessSchema
from ..user_role.entities import UserRole
from src.shared.manage_error import ManageErrorUtils, CodeError, TError

from ..user_role.db_services import UserRoleDBService
from flask.json import jsonify

class Role(Enum):
    ADMIN = 'administrateur'
    CONSULTANT = 'consultant'


class UserDBService:
    @staticmethod
    def get_all_users():
        session = None
        users = None
        try:
            session = Session()
            users_objects = session.query(*[c.label(c.name) for c in User.__table__.c if c.name != 'password_u'],
                                          (RoleAccess.nom_ra).label("roles")) \
                .join(UserRole, User.id_u == UserRole.id_u) \
                .join(RoleAccess, UserRole.id_ra == RoleAccess.id_ra) \
                .order_by(User.id_u.asc()) \
                .all()
            session.close()
            users = []
            for user in users_objects:
                user = {key: val for key, val in sorted(user._asdict().items(), key=lambda ele: ele[0])}
                user['roles'] = [user['roles']]
                user_found = next((sub for sub in users if sub['id_u'] == user['id_u']), None)
                if user_found:
                    user_index = users.index(user_found)
                    users[user_index]['roles'] += user['roles']
                else:
                    users.append(user)
            
            return users
        except Exception as e:
            current_app.logger.error(e)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_user_role_names_by_user_id_or_email(criteria):
        session = None
        returned_roles = []
        try:
            session = Session()
            int(criteria)
            roles = session.query(User, UserRole, RoleAccess) \
                .filter(User.id_u == UserRole.id_u, UserRole.id_ra == RoleAccess.id_ra, User.id_u == criteria) \
                .with_entities(RoleAccess.nom_ra).all()
        except ValueError:
            roles = session.query(User, UserRole, RoleAccess) \
                .filter(User.id_u == UserRole.id_u, UserRole.id_ra == RoleAccess.id_ra, User.email_u == criteria) \
                .with_entities(RoleAccess.nom_ra).all()
        finally:
            if session is not None:
                session.close()

            roles = RoleAccessSchema(many=True).dump(roles)
            for role in roles:
                returned_roles.append(role['nom_ra'])
            return returned_roles

    @staticmethod
    def get_user_by_id(user_id: int):
        session = None
        response = None
        try:
            session = Session()
            user_array = session.query(*[c.label(c.name) for c in User.__table__.c if c.name != 'password_u'], (RoleAccess.nom_ra).label('roles')) \
                .join(UserRole, User.id_u == UserRole.id_u) \
                .join(RoleAccess, UserRole.id_ra == RoleAccess.id_ra) \
                .filter(User.id_u == user_id) \
                .all()
            session.close()
            
            if user_array is None or len(user_array) == 0:
                ManageErrorUtils.value_error(CodeError.DATA_NOT_FOUND, TError.VALUE_ERROR, 'Cet utilisateur n\'existe pas', 404)
            else:
                for user in user_array:
                    user = {key: val for key, val in sorted(user._asdict().items(), key=lambda ele: ele[0])}
                    if response is None:
                        response = user
                        response['roles'] = [response['roles']]
                    else:
                        response['roles'].append(user['roles'])
            
            return response
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def get_user_by_email(user_email):
        session = Session()
        user_object = session.query(User).filter_by(email_u=user_email).first()

        schema = UserSchema(exclude=['password_u'])
        user = schema.dump(user_object)

        session.close()
        return user

    @staticmethod
    def check_unique_mail_and_initiales(user_id: int, email_u: str, initiales: str):
        session = None
        user_object = None
        try:
            session = Session()
            user_object = session.query(User) \
                .filter(User.id_u != user_id) \
                .filter(or_(User.email_u == email_u, User.initiales_u == initiales)) \
                .first()
            session.close()
            
            if user_object is not None:
                msg = "L'email '{}' ou les initiales '{}' sont déjà utilisé par un autre utilisateur".format(email_u, initiales)
                ManageErrorUtils.value_error(CodeError.UNIQUE_CONSTRAINT_ERROR, TError.VALUE_ERROR, msg, 409)
            return user_object
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def insert(user, old_roles: list, new_roles: list):
        session = None
        new_user = None
        try:
            for r in new_roles:
                role = (1 if r == Role.ADMIN.value else 2)
                if len(new_roles) > len(old_roles):
                    UserRoleDBService.insert_user_role(user.id_u, role)
                else:
                    UserRoleDBService.update_user_role(user.id_u, role)

            updated_user = UserSchema(exclude=['password_u']).dump(user)
            updated_user['roles'] = new_roles
            user = User(**updated_user)
            
            # Start DB session
            session = Session()
            session.add(user)
            session.commit()
            session.close()
    
            new_user = UserSchema(exclude=['password_u']).dump(user)
            return new_user
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def update(user, old_roles: list, new_roles: list):
        session = None
        update_user = None
        try:
            #TODO meme role plusieur fois check
            for r in new_roles:
                role = (1 if r == Role.ADMIN.value else 2)
                if len(new_roles) > len(old_roles):
                    UserRoleDBService.insert_user_role(user['id_u'], role)
                elif len(new_roles) < len(old_roles):
                    diff = np.setdiff1d(old_roles,new_roles)[0]
                    role = (1 if diff == Role.ADMIN.value else 2)
                    UserRoleDBService.delete_user_role(user['id_u'], role)
                    old_roles = list(set(old_roles) - set(diff))
                else:
                    UserRoleDBService.update_user_role(user['id_u'], role)

            updated_user = UserSchema(exclude=['password_u']).dump(user)
            user = User(**updated_user)
            
            # Start DB session
            session = Session()
            session.merge(user)
            session.commit()
            session.close()
    
            update_user = UserSchema(exclude=['password_u']).dump(user)
            update_user['roles'] = new_roles
            return update_user
        except ValueError as error:
            current_app.logger.error(error)
            raise
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def change_pwd(user_id: int, new_password: str):
        session = None
        response = None
        try:
            # Start DB session
            session = Session()
            user = session.query(User).get(user_id)
            user.password_u = User.generate_hash(new_password)
            session.commit()
            session.close()
    
            response = {'message': 'Le Password a été bien modifié'}
        finally:
            if session is not None:
                session.close()
            return response
    
    @staticmethod
    def is_responsable_of_projet(project_id: int):
        is_responsable = False
        project = ProjectDBService.get_project_by_id(project_id)
        user = UserDBService.get_user_by_email(get_jwt_identity())
        if project is not None and 'responsable' in project and \
                user is not None and 'id_u' in user \
                and user['id_u'] == project['responsable']['id_u']:
            role = UserDBService.get_user_role_names_by_user_id_or_email(user['id_u'])
            is_responsable = role[0] == Role.CONSULTANT.value
        return is_responsable

    @staticmethod
    def is_admin():
        is_admin = False
        user = UserDBService.get_user_by_email(get_jwt_identity())
        if user is not None and 'id_u' in user:
            role = UserDBService.get_user_role_names_by_user_id_or_email(user['id_u'])
            is_admin = role[0] == Role.ADMIN.value
        return is_admin

    @staticmethod
    def revoke_token(jti: str) -> RevokedToken or None:
        session = None
        revoked_token = None

        try:
            session = Session()
            r = RevokedToken(jti)
            session.add(r)
            session.commit()

            revoked_token = RevokedTokenSchema().dump(r)
        finally:
            session.close()

        return revoked_token

    @staticmethod
    def get_revoked_token_by_jti(jti: str):
        session = None
        token = None

        try:
            session = Session()
            token = session.query(RevokedToken).filter_by(jti=jti).first()
            token = RevokedTokenSchema().dump(token)
        finally:
            if session:
                session.close()

        return token
