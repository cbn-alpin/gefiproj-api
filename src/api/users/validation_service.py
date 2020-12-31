import re

ERROR_CODE = 'VALIDATION_ERROR'
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserValidationService:
    @staticmethod
    def validate_post(user):
        errors = []
        if not re.search(EMAIL_REGEX, user['email_u']):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'email_u',
                'message': 'Le champ <email_u> doit être un email valide',
            })
        return errors
