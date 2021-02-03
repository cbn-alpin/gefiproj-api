from enum import Enum

from flask_jwt_extended import get_jwt_identity

from src.shared.entity import Session
from .entities import User, UserSchema, RevokedToken, RevokedTokenSchema
from ..projects.db_service import ProjectDBService
from ..role_acces.entities import RoleAccess, RoleAccessSchema
from ..user_role.user_role import UserRole


class Role(Enum):
    ADMIN = 'administrateur'
    CONSULTANT = 'consultant'


class UserDBService:
    @staticmethod
    def get_user_role_names_by_user_id_or_email(criteria):
        session = None

        try:
            session = Session()
            int(criteria)
            roles = session.query(User, UserRole, RoleAccess) \
                .filter(User.id_u == UserRole.id_u) \
                .filter(UserRole.id_ra == RoleAccess.id_ra) \
                .filter(User.id_u == criteria) \
                .with_entities(RoleAccess.nom_ra).all()
        except ValueError:
            roles = session.query(User, UserRole, RoleAccess) \
                .filter(User.id_u == UserRole.id_u) \
                .filter(UserRole.id_ra == RoleAccess.id_ra) \
                .filter(User.email_u == criteria) \
                .with_entities(RoleAccess.nom_ra).all()
        finally:
            session.close()

        roles = RoleAccessSchema(many=True).dump(roles)
        returned_roles = []
        for role in roles:
            returned_roles.append(role['nom_ra'])
        return returned_roles

    @staticmethod
    def check_user_exists_by_id(user_id):
        try:
            session = Session()
            existing_user = session.query(User).filter_by(id_u=user_id).first()
            session.close()

            if existing_user is None:
                raise ValueError('This user does not exist')
            return existing_user
        except ValueError:
            resp = {
                'code': 'USER_NOT_FOUND',
                'message': f'User with id <{user_id}> does not exist.'
            }

            return resp

    @staticmethod
    def get_user_by_email(user_email):
        session = Session()
        user_object = session.query(User).filter_by(email_u=user_email).first()

        schema = UserSchema(only=['nom_u', 'prenom_u', 'initiales_u', 'active_u', 'id_u', 'email_u'])
        user = schema.dump(user_object)

        session.close()
        return user

    @staticmethod
    def get_user_by_initiales(user_initiales):
        session = Session()
        user_object = session.query(User).filter_by(initiales_u=user_initiales).first()

        user = UserDBService.process_get_user(user_object)

        session.close()
        return user

    @staticmethod
    def process_get_user(user_object):
        schema = UserSchema(only=['nom_u', 'prenom_u', 'initiales_u', 'active_u', 'id_u', 'email_u'])
        user = schema.dump(user_object)

        return user

    @staticmethod
    def insert_user(user: User, roles):
        session = None
        new_user = None

        try:
            session = Session()
            session.add(user)
            session.flush()

            for role in roles:
                role_id = 1
                if role == 'consultant':
                    role_id = 2
                session.execute("insert into role_utilisateur values (:role_id, :user_id)",
                                {'user_id': user.id_u, 'role_id': role_id})
            session.commit()

            new_user = UserSchema(only=['nom_u', 'prenom_u', 'initiales_u', 'active_u', 'id_u', 'email_u']) \
                .dump(user)
        finally:
            if session:
                session.close()

        return new_user

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

    @staticmethod
    def merge_user(user, data):
        user.nom_u = data['nom_u']
        user.prenom_u = data['prenom_u']
        user.email_u = data['email_u']
        user.initiales_u = data['initiales_u']
        user.active_u = data['active_u']

        return user
