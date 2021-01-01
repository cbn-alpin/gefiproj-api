from src.shared.entity import Session

from .entities import User, UserSchema
from ..role_acces.entities import RoleAccess, RoleAccessSchema
from ..user_role.user_role import UserRole


class UserDBService:
    @staticmethod
    def get_user_role_names_by_user_id_or_email(criteria):
        session = Session()

        try:
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

        schema = UserSchema()
        user = schema.dump(user_object)

        if user:
            user.pop('password_u', None)

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
        schema = UserSchema()
        user = schema.dump(user_object)

        if user:
            user.pop('password_u', None)

        return user

    @staticmethod
    def insert_user(user):
        session = Session()
        session.add(user)
        session.commit()

        new_user = UserSchema().dump(user)
        if new_user:
            new_user.pop('password_u', None)

        session.close()
        return new_user
