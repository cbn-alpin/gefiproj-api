from shared.entity import Session

from .entities import User


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
