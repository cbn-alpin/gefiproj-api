import unittest

from src.api.users.validation_service import UserValidationService


class UserValidationServiceTestCase(unittest.TestCase):
    def test_validate_post(self):
        user1 = {'nom_u': 'Samaké', 'prenom_u': 'Zantiè', 'initiales_u': 'zas',
                 'email_u': 'zantie.samake@mail.ml',
                 'password_u': 'zan@password', 'active_u': True}
        validation_errors = UserValidationService.validate_post(user1)
        self.assertEqual(len(validation_errors), 0)

        user2 = {'prenom_u': 'Zantiè', 'initiales_u': 'zas',
                 'email_u': 'zantie.samake@mail.ml',
                 'password_u': 'zan@password', 'active_u': True}
        validation_errors = UserValidationService.validate_post(user2)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['type'], 'MISSING_PARAMETER')
        self.assertEqual(validation_errors[0]['field'], 'nom_u')

        user3 = {'nom_u': 'Samaké', 'prenom_u': 'Zantiè', 'initiales_u': 'zas',
                 'email_u': 'zantie.samake@mail',
                 'password_u': 'zan@password', 'active_u': True}
        validation_errors = UserValidationService.validate_post(user3)
        self.assertEqual(len(validation_errors), 1)
        self.assertEqual(validation_errors[0]['type'], 'VALUE_ERROR')
        self.assertEqual(validation_errors[0]['field'], 'email_u')
