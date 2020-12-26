from src.shared.entity import Session

from .entities import User
from ..role_acces.entities import RoleAccess, RoleAccessSchema
from ..user_role.user_role import UserRole


class UserDBService:
    @staticmethod
    def get_user_role_names_by_user_id(user_id: int):
        session = Session()
        roles = session.query(User, UserRole, RoleAccess) \
            .filter(User.id_u == UserRole.id_u) \
            .filter(UserRole.id_ra == RoleAccess.id_ra) \
            .filter(User.id_u == user_id) \
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
