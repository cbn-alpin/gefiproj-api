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
            ManageCheckDataUtils.check_format_value('code_p', project, int, 'code projet')
            ManageCheckDataUtils.check_format_value('nom_p', project, str, 'nom')
            ManageCheckDataUtils.check_string_lenght('nom_p', 'nom', project, 3, 250)
            ManageCheckDataUtils.check_format_value('statut_p', project, bool, 'statut')
            ManageCheckDataUtils.check_format_value('id_u', project, int, 'responsable')
            
            ManageCheckDataUtils.check_not_none('code_p', project, 'code projet')
            ManageCheckDataUtils.check_not_none('id_u', project, 'responsable')
        except ValueError as error:
            current_app.logger.error(f"ProjectValidationService - validate_form : {error}")
            raise

    @staticmethod
    def validate_get_all(query_params):
        try:
            if 'limit' in query_params:
                # limit validation
                ManageCheckDataUtils.check_format_value('limit', query_params, int, 'limit')
            if 'offset' in query_params:
                # offset validation
                ManageCheckDataUtils.check_format_value('offset', query_params, int, 'offset')
        except ValueError as error:
            current_app.logger.error(f"ProjectValidationService - validate_get_all : {error}")
            raise
