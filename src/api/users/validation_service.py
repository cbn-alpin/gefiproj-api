from src.shared.manage_check_data import ManageCheckDataUtils, CodeError, TError
from flask import current_app

KEYS = ['nom_u', 'prenom_u', 'initiales_u', 'email_u', 'active_u', 'roles']
ROLES = ['administrateur', 'consultant']

        
class UserValidationService:
    @staticmethod
    def validate_login(data):
        try:
            # validation keys
            ManageCheckDataUtils.check_keys(['login', 'password'], data)
            ManageCheckDataUtils.check_format_value('login', data, str, 'email')
            ManageCheckDataUtils.check_format_value('password', data, str, 'mot de passe')
            ManageCheckDataUtils.check_not_none('password', data, 'mot de passe')
        except ValueError as error:
            current_app.logger.warning(error)
            raise

    @staticmethod
    def validate_change_pwd(data):
        try:
            # validation keys
            ManageCheckDataUtils.check_keys(['new_password'], data)
            ManageCheckDataUtils.check_string_lenght('new_password', 'mot de passe', data, 5)
        except ValueError as error:
            current_app.logger.warning(error)
            raise

    @staticmethod
    def validate_post(user):
        try:
            user_keys = ['password_u']
            # validation keys
            ManageCheckDataUtils.check_keys(user_keys, user)
            ManageCheckDataUtils.check_string_lenght('password_u', 'mot de passe', user, 5)
            # validate_update
            UserValidationService.validate_update(user)
        except ValueError as error:
            current_app.logger.warning(error)
            raise
        
    @staticmethod
    def validate_update(user):
        try:
            user_keys = KEYS
            # validation keys
            ManageCheckDataUtils.check_keys(user_keys, user)
            # validation format
            ManageCheckDataUtils.check_format_value('nom_u', user, str, 'nom')
            ManageCheckDataUtils.check_format_value('prenom_u', user, str, 'prénom')
            ManageCheckDataUtils.check_format_value('initiales_u', user, str, 'initiales')
            ManageCheckDataUtils.check_format_value('email_u', user, str, 'email')
            ManageCheckDataUtils.check_format_mail('email_u', user, 'email')
            ManageCheckDataUtils.check_format_value('active_u', user, bool, 'active')
            ManageCheckDataUtils.check_format_array('roles', user, 2, 'roles')
            ManageCheckDataUtils.check_array_is_subset('roles', user['roles'], ROLES, 'roles')
            ManageCheckDataUtils.check_duplicate_value('roles', user, 'roles')
            
            ManageCheckDataUtils.check_not_none('nom_u', user, 'nom')
            ManageCheckDataUtils.check_not_none('prenom_u', user, 'prénom')
            ManageCheckDataUtils.check_not_none('initiales_u', user, 'initiales')
            ManageCheckDataUtils.check_not_none('email_u', user, 'email')
        except ValueError as error:
            current_app.logger.warning(error)
            raise
