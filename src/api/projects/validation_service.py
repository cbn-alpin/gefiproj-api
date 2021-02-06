from src.shared.manage_check_data import ManageCheckDataUtils
from flask import current_app

KEYS = ['code_p', 'nom_p', 'statut_p', 'id_u']

class ProjectValidationService:
    @staticmethod
    def validate_form(project):
        try:
            project_keys = KEYS
            # validation keys
            ManageCheckDataUtils.check_keys(project_keys, project)
            # validation format
            ManageCheckDataUtils.check_format_value('code_p', project, int)
            ManageCheckDataUtils.check_format_value('nom_p', project, str)
            ManageCheckDataUtils.check_string_lenght('nom_p', project, 3, 250)
            ManageCheckDataUtils.check_format_value('statut_p', project, bool)
            ManageCheckDataUtils.check_format_value('id_u', project, int)
        except ValueError as error:
            current_app.logger.warning(error)
            raise

    @staticmethod
    def validate_get_all(query_params):
        try:
            if 'limit' in query_params:
                # limit validation
                ManageCheckDataUtils.check_format_value('limit', query_params, int)
            if 'offset' in query_params:
                # offset validation
                ManageCheckDataUtils.check_format_value('offset', query_params, int)
        except ValueError as error:
            current_app.logger.warning(error)
            raise
