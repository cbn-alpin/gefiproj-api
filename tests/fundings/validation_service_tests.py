import unittest

from src.api.fundings.validation_service import FundingValidationService


class ProjectValidationServiceTestCase(unittest.TestCase):
    def test_validate_post(self):
        funding = {'id_f': 1, 'id_p': 1, 'id_financeur': 1, 'montant_arrete_f': 4, 'statut_f': 'ANTR'}
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 0)

        funding['statut_f'] = 'SOLDE'
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'statut_f')
        funding['statut_f'] = 'ANTR'

        del funding['id_p']
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'id_p')
        funding['id_p'] = 1
        
        del funding['id_financeur']
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'id_financeur')
        funding['id_financeur'] = 1
        
        del funding['montant_arrete_f']
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'montant_arrete_f')
        funding['montant_arrete_f'] = 10
        
        del funding['statut_f']
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'statut_f')
        funding['statut_f'] = 'ANTR'

        funding['statut_f'] = 'NO'
        validation_errors = FundingValidationService.validate_post(funding)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['field'], 'statut_f')
        funding['statut_f'] = 'ANTR'

if __name__ == '__main__':
    unittest.main()
