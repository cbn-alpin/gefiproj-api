import re

from src.shared.data_validation_utils import DataValidationUtils, ERROR_CODE

EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserValidationService:
    @staticmethod
    def validate_post(user):
        errors = []

        user_keys = ['nom_u', 'prenom_u', 'initiales_u', 'email_u', 'password_u', 'active_u']
        errors = DataValidationUtils.check_keys(user_keys, user)

        if 'email_u' in user \
                and not re.search(EMAIL_REGEX, user['email_u']):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'email_u',
                'message': 'Parameter <email_u> must be a valid email address',
            })
        return errors
