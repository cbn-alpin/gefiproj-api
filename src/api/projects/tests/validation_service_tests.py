import unittest

from src.api.projects.validation_service import ProjectValidationService


class ProjectValidationServiceTestCase(unittest.TestCase):
    def test_validate_get_all(self):
        validation_errors = ProjectValidationService.validate_get_all({'limit': 'some limit', 'offset': 'some offset'})
        self.assertEqual(len(validation_errors), 2)

        validation_errors = ProjectValidationService.validate_get_all({'limit': '10', 'offset': '20'})
        self.assertEqual(len(validation_errors), 0)

    def test_validate_post(self):
        project = {'code_p': 'test', 'nom_p': 'Project TEST', 'statut_p': 'true', 'id_u': 4}
        validation_errors = ProjectValidationService.validate_post(project)
        self.assertEqual(len(validation_errors), 0)

        project['statut_p'] = 'terminé'
        validation_errors = ProjectValidationService.validate_post(project)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'statut_p')


if __name__ == '__main__':
    unittest.main()
