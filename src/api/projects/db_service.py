from sqlalchemy.orm import subqueryload

from src.shared.entity import Session
from .entities import Project, ProjectSchema

project_not_exist_msg = 'This projcet does not exist'


class ProjectDBService:
    @staticmethod
    def insert_project(project: Project):
        session = Session()
        session.add(project)
        session.commit()

        new_project = ProjectSchema().dump(project)
        session.close()
        return new_project

    @staticmethod
    def get_all_projects(limit=10, offset=0):
        session = Session()
        projects_objects = session.query(Project) \
            .options(
            subqueryload(Project.responsable)
        ).limit(limit).offset(offset).all()

        # Transforming into JSON-serializable objects
        schema = ProjectSchema(many=True)
        projects = schema.dump(projects_objects)

        for p in projects:
            p.pop('id_u', None)
            p['responsable'].pop('password_u', None)

        # Serializing as JSON
        session.close()
        return projects

    @staticmethod
    def get_project_by_id(proj_id: int):
        session = Session()
        project_object = session.query(Project) \
            .options(subqueryload(Project.responsable)) \
            .filter_by(id_p=proj_id).first()

        # Transforming into JSON-serializable objects
        schema = ProjectSchema()
        project = schema.dump(project_object)

        if project:
            project.pop('id_u', None)
            project['responsable'].pop('password_u', None)

        # Serializing as JSON
        session.close()
        return project

    @staticmethod
    def get_project_by_code(code_p: str):
        session = Session()
        project_object = session.query(Project).filter_by(code_p=code_p).first()

        schema = ProjectSchema(many=False)
        project = schema.dump(project_object)

        session.close()
        return project

    @staticmethod
    def get_project_by_nom(nom_p: str):
        session = Session()
        project_object = session.query(Project).filter_by(nom_p=nom_p).first()

        schema = ProjectSchema(many=False)
        project = schema.dump(project_object)

        session.close()
        return project

    @staticmethod
    def update_project(project: Project):
        session = Session()
        session.merge(project)
        session.commit()

        updated_project = ProjectSchema().dump(project)
        session.close()
        return updated_project

    @staticmethod
    def delete_project(project_id: int) -> int:
        session = Session()
        session.query(Project).filter_by(id_p=project_id).delete()
        session.commit()
        session.close()

        return project_id

    @staticmethod
    def check_project_exists_by_id(proj_id: int):
        existing_proj = ProjectDBService.get_project_by_id(proj_id)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJECT_NOT_FOUND',
                'message': f'Project with id <{proj_id}> does not exist.'
            }

            return msg

    @staticmethod
    def check_project_exists_by_name(project_name: str):
        existing_proj = ProjectDBService.get_project_by_nom(project_name)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJECT_NOT_FOUND',
                'message': f'Project with name <{project_name}> does not exist.'
            }

            return msg

    @staticmethod
    def check_project_exists_by_code(project_code):
        existing_proj = ProjectDBService.get_project_by_code(project_code)
        if 'id_p' not in existing_proj:
            msg = {
                'code': 'PROJECT_NOT_FOUND',
                'message': f'Project with code <{project_code}> does not exist.'
            }

            return msg
