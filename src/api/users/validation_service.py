import re

ERROR_CODE = 'VALIDATION_ERROR'
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserValidationService:
    @staticmethod
    def check_keys(keys: [], user):
        errors = []

        for key in keys:
            if key not in user:
                errors.append({
                    'code': ERROR_CODE,
                    'type': 'MISSING_PARAMETER',
                    'field': key,
                    'message': 'Paramter <{}> is missing'.format(key),
                })
        return errors

    @staticmethod
    def validate_post(user):
        errors = []

        user_keys = ['nom_u', 'prenom_u', 'initiales_u', 'email_u', 'password_u', 'active_u']
        errors = UserValidationService.check_keys(user_keys, user)

        if 'email_u' in user \
                and not re.search(EMAIL_REGEX, user['email_u']):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'email_u',
                'message': 'Parameter <email_u> must be a valid email address',
            })
        return errors
