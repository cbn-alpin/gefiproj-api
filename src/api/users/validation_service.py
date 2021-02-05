ERROR_CODE = "VALISATION ERROR"

from src.shared.manage_check_data import ManageCheckDataUtils, CodeError, TError
from flask import current_app

KEYS = ['nom_u', 'prenom_u', 'initiales_u', 'email_u', 'active_u', 'roles']
ROLES = ['administrateur', 'consultant']

        
class UserValidationService:
    @staticmethod
    def validate_change_pwd(data):
        try:
            # validation keys
            ManageCheckDataUtils.check_keys(['new_password'], data)
            ManageCheckDataUtils.check_string_sup_lenght('new_password', data, 5)
        except ValueError as error:
            current_app.logger.error(error)
            raise

    @staticmethod
    def validate_post(user):
        try:
            user_keys = KEYS
            user_keys.append(['password_u'])
            # validation keys
            ManageCheckDataUtils.check_keys(user_keys, user)
            # validate_update
            UserValidationService.validate_update(user)
        except ValueError as error:
            current_app.logger.error(error)
            raise
        
    @staticmethod
    def validate_update(user):
        try:
            user_keys = KEYS
            # validation keys
            ManageCheckDataUtils.check_keys(user_keys, user)
            # validation format
            ManageCheckDataUtils.check_format_value('nom_u', user, str)
            ManageCheckDataUtils.check_format_value('prenom_u', user, str)
            ManageCheckDataUtils.check_format_value('initiales_u', user, str)
            ManageCheckDataUtils.check_format_value('email_u', user, str)
            ManageCheckDataUtils.check_format_mail('email_u', user)
            ManageCheckDataUtils.check_format_value('active_u', user, bool)
            ManageCheckDataUtils.check_format_array('roles', user, list, 2)
            ManageCheckDataUtils.check_array_is_subset('roles', user['roles'], ROLES)
        except ValueError as error:
            current_app.logger.warning(error)
            raise
