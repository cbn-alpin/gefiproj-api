import unittest

from src.api.receipts.validation_service import ReceiptValidationService


class ReceiptValidationServiceTestCase(unittest.TestCase):
    def test_validate_post_missing_annee_r(self):
        receipt_data = {'id_f': 4, 'montant_r': 3095.7}
        validation_errors = ReceiptValidationService.validate_post(receipt_data)

        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'annee_r')
        self.assertEqual(validation_errors[0]['type'], 'MISSING_PARAMETER')

    def test_validate_post_invalid_montant_r(self):
        receipt_data = {'id_f': '7', 'montant_r': -7095.7, 'annee_r': '2018'}
        validation_errors = ReceiptValidationService.validate_post(receipt_data)

        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'montant_r')
        self.assertEqual(validation_errors[0]['type'], 'VALUE_ERROR')

    def test_validate_post_invalid_annee_r(self):
        receipt_data = {'id_f': '7', 'montant_r': 9015.7, 'annee_r': 'hier'}
        validation_errors = ReceiptValidationService.validate_post(receipt_data)

        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'annee_r')
        self.assertEqual(validation_errors[0]['type'], 'VALUE_ERROR')

    def test_validate_post_ok(self):
        receipt_data = {'id_f': '7', 'montant_r': '1037.9', 'annee_r': '2020'}
        validation_errors = ReceiptValidationService.validate_post(receipt_data)

        self.assertEqual(len(validation_errors), 0)


if __name__ == '__main__':
    unittest.main()
