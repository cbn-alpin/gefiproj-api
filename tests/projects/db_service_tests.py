import unittest

from marshmallow import EXCLUDE

from src.api.projects.db_service import ProjectDBService
from src.api.projects.entities import Project, ProjectSchema
from src.shared.test_base import DBBaseTestCase


# Postgresql unittest example: https://github.com/axelcdv/flask-testing/


class DBServiceTestCase(DBBaseTestCase):
    def test_insert_project(self):
        new_project = {'nom_p': 'Haut de chèvre', 'code_p': '210001', 'statut_p': True, 'id_u': 1}
        inserted_project = ProjectDBService.insert(new_project)

        project_object = self.db.session.query(Project).filter_by(id_p=inserted_project.get('id_p')).first()
        project_found = ProjectSchema().dump(project_object)
        self.assertEqual(inserted_project.get('id_p'), project_found.get('id_p'))
        self.assertEqual(inserted_project['code_p'], project_found.get('code_p'))
        self.db.session.query(Project).filter_by(id_p=new_project.get('id_p')).delete()
        self.db.session.commit()

    def test_get_project_by_id(self):
        with self.assertRaises(Exception):
            ProjectDBService.get_project_by_id(10)

        new_project = Project(nom_p='Testing', code_p='210077', statut_p=True, id_u=1)
        self.db.session.add(new_project)
        self.db.session.commit()
        project = ProjectDBService.get_project_by_id(new_project.id_p)
        self.assertEqual(project['id_p'], new_project.id_p)

    def test_get_all_projects(self):
        all_projects = ProjectDBService.get_all_projects()
        self.assertEqual(len(all_projects), 0)

        new_project1 = Project(nom_p='ça teste', code_p='210001', statut_p=True, id_u=1)
        new_project2 = Project(nom_p='OC10 test', code_p='210010', statut_p=True, id_u=1)
        self.db.session.bulk_save_objects([new_project1, new_project2])
        self.db.session.commit()

        all_projects = ProjectDBService.get_all_projects()
        self.assertEqual(len(all_projects), 2)

    def test_update_project(self):
        new_project_object = {'nom_p': 'X-files', 'code_p': '210007', 'statut_p': False, 'id_u': 1}
        new_project = ProjectSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u', 'id_p')) \
            .load(new_project_object, unknown=EXCLUDE)
        pr = Project(**new_project)
        self.db.session.add(pr)
        self.db.session.commit()

        new_project_object['id_p'] = pr.id_p
        new_project_object['statut_p'] = True
        new_project_object['nom_p'] = 'Lazy dog'

        updated_project = ProjectDBService.update(new_project_object)

        self.assertEqual(updated_project.get('id_p'), pr.id_p)
        self.assertEqual(updated_project.get('nom_p'), 'Lazy dog')
        self.assertTrue(updated_project.get('statut_p'))

        self.db.session.query(Project).filter_by(id_p=pr.id_p).delete()
        self.db.session.commit()

    # TODO: test the other methods


if __name__ == '__main__':
    unittest.main()
