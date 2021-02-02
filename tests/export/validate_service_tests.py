import unittest

from src.api.exports.validation_service import ExportValidationService


class MyTestCase(unittest.TestCase):
    def test_validate_export_ok(self):
        export_params_data = {
            'version': 1,
            'annee_ref': 2020,
            'partages': [
                {
                    'email': 'email@mail.ml',
                    'type': 'user',
                    'permission': 'writer'
                },
                {
                    'email': 'hismail@mail.ml',
                    'type': 'user',
                    'permission': 'writer'
                }
            ],
            'entete': ['Col1', 'Col2', 'Col3']
        }

        validation_errors = ExportValidationService.validate(export_params_data)
        self.assertEqual(0, len(validation_errors))

    def test_validate_export_invalid_shares(self):
        export_params_data = {
            'version': 1,
            'annee_ref': 2020,
            'partages': [
                {
                    'email': 'email@mail.ml',
                    'type': 'user',
                },
            ],
            'entete': ['Col1', 'Col2', 'Col3']
        }

        validation_errors = ExportValidationService.validate(export_params_data)
        self.assertEqual(1, len(validation_errors))

    def test_validate_export_invalid_version(self):
        export_params_data = {
            'annee_ref': 2020,
            'partages': [
                {
                    'email': 'email@mail.ml',
                    'type': 'user',
                    'permission': 'writer'
                },
            ],
            'entete': ['Col1', 'Col2', 'Col3'],
            'version': 3,
        }

        validation_errors = ExportValidationService.validate(export_params_data)
        self.assertEqual('version', validation_errors[0]['field'])
        self.assertEqual(1, len(validation_errors))

        # missing annee_max
        export_params_data['version'] = 2
        validation_errors = ExportValidationService.validate(export_params_data)
        self.assertEqual(1, len(validation_errors))
        self.assertEqual('anne_max', validation_errors[0]['field'])


if __name__ == '__main__':
    unittest.main()
