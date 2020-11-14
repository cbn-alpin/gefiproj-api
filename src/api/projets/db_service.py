from shared.entity import Session

from .entities import Projet

project_not_exist_msg = 'This projet does not exist'


def check_projet_exists_by_id(proj_id: int):
    try:
        session = Session()
        existing_proj = session.query(Projet).filter_by(id_p=proj_id).first()
        session.close()
        if existing_proj is None:
            raise ValueError(project_not_exist_msg)
    except ValueError:
        msg = {
            'code': 'PROJET_NOT_FOUND',
            'message': f'Projet with id <{proj_id}> does not exist.'
        }

        return msg


def check_projet_exists_by_name(project_name: str):
    try:
        session = Session()
        existing_proj = session.query(Projet).filter_by(nom_p=project_name).first()
        session.close()
        if existing_proj is None:
            raise ValueError(project_not_exist_msg)
    except ValueError:
        msg = {
            'code': 'PROJET_NOT_FOUND',
            'message': f'Projet with name <{project_name}> does not exist.'
        }

        return msg


def check_projet_exists_by_code(project_code):
    try:
        session = Session()
        existing_proj = session.query(Projet).filter_by(code_p=project_code).first()
        session.close()
        if existing_proj is None:
            raise ValueError(project_not_exist_msg)
    except ValueError:
        msg = {
            'code': 'PROJET_NOT_FOUND',
            'message': f'Projet with code <{project_code}> does not exist.'
        }

        return msg
