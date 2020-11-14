from shared.entity import Session

from .entities import Projet, ProjetSchema

project_not_exist_msg = 'This projet does not exist'


class ProjectDBService():
    @staticmethod
    def insert_projet(projet: Projet):
        session = Session()
        session.add(projet)
        session.commit()

        new_projet = ProjetSchema().dump(projet)
        return new_projet

    @staticmethod
    def get_all_projets(limit=10, offset=0):
        session = Session()
        projets_objects = session.query(Projet) \
            .limit(limit).offset(offset).all()

        # Transforming into JSON-serializable objects
        schema = ProjetSchema(many=True)
        projets = schema.dump(projets_objects)

        # Serializing as JSON
        session.close()
        return projets

    @staticmethod
    def get_projet_by_id(proj_id: int):
        session = Session()
        projet_object = session.query(Projet).filter_by(id_p=proj_id).all()

        # Transforming into JSON-serializable objects
        schema = ProjetSchema(many=True)
        projet = schema.dump(projet_object)

        # Serializing as JSON
        session.close()
        return projet

    @staticmethod
    def update_projet(projet: Projet):
        session = Session()
        session.merge(projet)
        session.commit()

        updated_projet = ProjetSchema().dump(projet)
        session.close()
        return updated_projet

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
