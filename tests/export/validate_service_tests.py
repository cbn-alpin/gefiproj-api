import unittest

from src.api.exports.validation_service import ExportValidationService


class MyTestCase(unittest.TestCase):
    def test_validate_export_ok(self):
        export_params_data = {
            'annee_ref': 2020,
            'shares': [
                {
                    'email': 'email@mail.ml',
                    'type': 'user',
                    'permission': 'write'
                },
                {
                    'email': 'hismail@mail.ml',
                    'type': 'user',
                    'permission': 'write'
                }
            ],
            'headers': ['Col1', 'Col2', 'Col3']
        }

        validation_errors = ExportValidationService.validate_v1(export_params_data)
        self.assertEqual(0, len(validation_errors))

    def test_validate_export_invalid_shares(self):
        export_params_data = {
            'annee_ref': 2020,
            'shares': [
                {
                    'email': 'email@mail.ml',
                    'type': 'user',
                },
            ],
            'headers': ['Col1', 'Col2', 'Col3']
        }

        validation_errors = ExportValidationService.validate_v1(export_params_data)
        self.assertEqual(1, len(validation_errors))


if __name__ == '__main__':
    unittest.main()
