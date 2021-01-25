import unittest

from src.api.projects.entities import Project, ProjectSchema


class EntitiesTestCase(unittest.TestCase):
    def test_project_entity(self):
        project = Project(210003, 'Project étoile', 'true', 4)
        self.assertEqual(project.code_p, 210003)
        self.assertEqual(project.nom_p, 'Project étoile')
        self.assertEqual(project.statut_p, 'true')
        self.assertEqual(project.id_u, 4)

    def test_project_entity_with_responsable(self):
        responsable = {
            'id_u': 5,
            'nom_u': 'Walker',
            'prenom_u': 'Kal',
            'initiales_u': 'res',
            'email_u': 'mail@mail.ml',
            'active_u': False
        }
        project = Project('test', 'Project TEST', 'true', 4, responsable=responsable)
        self.assertEqual(project.responsable, responsable)

    def test_project_schema(self):
        schema = ProjectSchema()
        data = schema.load({'code_p': 210009, 'nom_p': 'Project TEST', 'statut_p': 'true', 'id_u': 4})
        project = Project(**data)

        self.assertEqual(project.code_p, 210009)
        self.assertEqual(project.nom_p, 'Project TEST')
        self.assertEqual(project.statut_p, True)
        self.assertEqual(project.id_u, 4)


if __name__ == '__main__':
    unittest.main()
