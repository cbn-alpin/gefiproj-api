import re

from src.shared.data_validation_utils import DataValidationUtils, ERROR_CODE

EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserValidationService:
    @staticmethod
    def validate_change_pwd(data, is_admin):
        errors = DataValidationUtils.check_keys(['new_password'], data)
        if 'new_password' in data and len(data['new_password']) < 5:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'email_u',
                'message': 'Password too short',
            })
        if not is_admin:
            errors = errors + DataValidationUtils.check_keys(['password'], data)

        return errors

    @staticmethod
    def validate_post(user):
        errors = UserValidationService.validate_update(user)

        user_keys = ['password_u']
        errors = errors + DataValidationUtils.check_keys(user_keys, user)

        return errors

    @staticmethod
    def validate_update(user):
        errors = []

        user_keys = ['nom_u', 'prenom_u', 'initiales_u', 'email_u', 'active_u', 'roles']
        errors = DataValidationUtils.check_keys(user_keys, user)

        if 'email_u' in user \
                and not re.search(EMAIL_REGEX, user['email_u']):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'email_u',
                'message': 'Parameter <email_u> must be a valid email address',
            })

        if 'roles' in user:
            errors = DataValidationUtils.check_list('roles', user, errors)

            if len(user['roles']) > 2:
                errors.append({
                    'code': ERROR_CODE,
                    'type': 'VALUE_ERROR',
                    'field': 'roles',
                    'message': 'Parameter <roles> must be an array of at most 2 items',
                })
            else:
                for role in user['roles']:
                    if role != 'consultant' and role != 'administrateur':
                        errors.append({
                            'code': ERROR_CODE,
                            'type': 'VALUE_ERROR',
                            'field': 'roles',
                            'message': 'Parameter <roles> must be either <consultant> or <administrateur>',
                        })
        return errors
