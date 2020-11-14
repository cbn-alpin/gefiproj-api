from shared.entity import Session

from .entities import Projet


def check_projet_exists_by_id(proj_id):
    try:
        session = Session()
        existing_proj = session.query(Projet).filter_by(id_p=proj_id).first()
        session.close()
        if existing_proj is None:
            raise ValueError('This projet does not exist')
    except ValueError:
        msg = {
            'code': 'PROJET_NOT_FOUND',
            'message': f'Projet with id {proj_id} does not exist.'
        }

        return msg
