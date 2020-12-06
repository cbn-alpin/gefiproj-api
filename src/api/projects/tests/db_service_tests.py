import unittest

from src.api.projects.db_service import ProjectDBService
# Postgresql unittest example: https://github.com/axelcdv/flask-testing/
from src.shared.test_base import DBBaseTestCase


class DBServiceTestCase(DBBaseTestCase):
    def test_get_project_by_id(self):
        project = ProjectDBService.get_project_by_id(0)
        self.assertEqual(project, {})

        # TODO: using test database insert an element then get it
        project = ProjectDBService.get_project_by_id(1)
        self.assertEqual(project['id_p'], 1)

    def test_get_all_projects(self):
        with self.app.app_context():
            projects = ProjectDBService.get_all_projects()
            self.assertGreaterEqual(len(projects), 0)

    def test_get_project_name(self):
        with self.app.app_context():
            project = ProjectDBService.get_project_by_id(100)
            self.assertEqual(project, {})

            project = ProjectDBService.get_project_by_id(1)
            self.assertEqual(project['id_p'], 1)


if __name__ == '__main__':
    unittest.main()
