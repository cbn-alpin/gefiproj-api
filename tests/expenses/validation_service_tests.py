import unittest

from src.api.expenses.validation_service import ExpenseValidationService


class ExpenseValidationServiceTestCase(unittest.TestCase):
    def test_validate_post_string_annee_d(self):
        validation_errors = ExpenseValidationService.validate_post({'annee_d': '20O0', 'montant_d': 56})
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'annee_d')

    def test_validate_post_empty_string_montant_d(self):
        validation_errors = ExpenseValidationService.validate_post({'annee_d': '2001', 'montant_d': ''})
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'montant_d')

    def test_validate_post_negative_values(self):
        validation_errors = ExpenseValidationService.validate_post({'annee_d': '2001', 'montant_d': -653})
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'montant_d')

        validation_errors = ExpenseValidationService.validate_post({'annee_d': '-2020', 'montant_d': 56})
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'annee_d')

    def test_validate_post_ok(self):
        validation_errors = ExpenseValidationService.validate_post({'annee_d': '2001', 'montant_d': '56.4'})
        self.assertEqual(len(validation_errors), 0)
