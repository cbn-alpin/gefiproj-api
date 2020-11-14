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
        projet_object = session.query(Projet).filter_by(id_p=proj_id).first()

        # Transforming into JSON-serializable objects
        schema = ProjetSchema(many=False)
        projet = schema.dump(projet_object)

        # Serializing as JSON
        session.close()
        return projet

    @staticmethod
    def get_projet_by_code(code_p: str):
        session = Session()
        projet_object = session.query(Projet).filter_by(code_p=code_p).first()

        schema = ProjetSchema(many=False)
        projet = schema.dump(projet_object)

        session.close()
        return projet

    @staticmethod
    def get_projet_by_nom(nom_p: str):
        session = Session()
        projet_object = session.query(Projet).filter_by(nom_p=nom_p).first()

        schema = ProjetSchema(many=False)
        projet = schema.dump(projet_object)

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
        existing_proj = ProjectDBService.get_projet_by_id(proj_id)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJET_NOT_FOUND',
                'message': f'Projet with id <{proj_id}> does not exist.'
            }

            return msg

    @staticmethod
    def check_projet_exists_by_name(project_name: str):
        existing_proj = ProjectDBService.get_projet_by_nom(project_name)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJET_NOT_FOUND',
                'message': f'Projet with name <{project_name}> does not exist.'
            }

            return msg

    @staticmethod
    def check_projet_exists_by_code(project_code):
        existing_proj = ProjectDBService.get_projet_by_code(project_code)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJET_NOT_FOUND',
                'message': f'Projet with code <{project_code}> does not exist.'
            }

            return msg

    @staticmethod
    def get_total_count():
        session = Session()
        count = session.query(Projet).count()
        session.close()
        return count
