import unittest

from src.api.projects.db_service import ProjectDBService
from src.api.projects.entities import Project, ProjectSchema
from src.shared.test_base import DBBaseTestCase


# Postgresql unittest example: https://github.com/axelcdv/flask-testing/


class DBServiceTestCase(DBBaseTestCase):
    def test_get_project_by_id(self):
        project = ProjectDBService.get_project_by_id(10)
        self.assertEqual(project, {})

        new_project = Project(nom_p='auto test', code_p='OC77', statut_p=True, id_u=1)
        self.db.session.add(new_project)
        self.db.session.commit()
        project = ProjectDBService.get_project_by_id(new_project.id_p)
        self.assertEqual(project['id_p'], new_project.id_p)

    def test_get_all_projects(self):
        all_projects = ProjectDBService.get_all_projects()
        self.assertEqual(len(all_projects), 0)

        new_project1 = Project(nom_p='auto test', code_p='OC01', statut_p=True, id_u=1)
        new_project2 = Project(nom_p='OC10 test', code_p='OC10', statut_p=True, id_u=1)
        self.db.session.bulk_save_objects([new_project1, new_project2])
        self.db.session.commit()

        all_projects = ProjectDBService.get_all_projects()
        self.assertEqual(len(all_projects), 2)

    def test_insert_project(self):
        new_project = Project(nom_p='auto test', code_p='OC01', statut_p=True, id_u=1)
        inserted_project = ProjectDBService.insert_project(new_project)

        project_object = self.db.session.query(Project).filter_by(id_p=new_project.id_p).first()
        project_found = ProjectSchema().dump(project_object)
        self.assertEqual(inserted_project['id_p'], project_found['id_p'])
        self.assertEqual(inserted_project['code_p'], project_found['code_p'])

    def test_get_project_name(self):
        project = ProjectDBService.get_project_by_id(100)
        self.assertEqual(project, {})

    # TODO: test the other methods


if __name__ == '__main__':
    unittest.main()
