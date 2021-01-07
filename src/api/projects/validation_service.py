ERROR_CODE = 'VALIDATION_ERROR'


class ProjectValidationService:
    @staticmethod
    def validate_post(project):
        errors = []

        # project id validation
        try:
            if 'id_p' in project:
                int(project['id_p'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_p',
                'message': '<id_p> must be a number',
            })

        # user id validation
        if 'id_u' not in project:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'id_u',
                'message': 'Parameter <id_u> is missing',
            })

        try:
            if 'id_u' in project:
                int(project['id_u'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_u',
                'message': '<id_u> must be a number',
            })

        # code validation
        if 'code_p' not in project:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'code_p',
                'message': 'Paramter <code_p> is missing',
            })

        if 'code_p' in project and len(project['code_p']) > 4:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'code_p',
                'message': '<code_p> must be at most 4 char',
            })

        # statut validation
        if 'statut_p' not in project:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'statut_p',
                'message': 'Parameter <statut_p> is missing',
            })

        if 'statut_p' in project and project['statut_p'] not in [False, True]:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'statut_p',
                'message': '<statut_p> must be either <True> or <False>',
            })

        # nom validation
        if 'nom_p' not in project:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'nom_p',
                'message': 'Parameter <nom_p> is missing',
            })

        if 'nom_p' in project and (len(project['nom_p']) < 3 or len(project['nom_p']) > 250):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'nom_p',
                'message': '<nom_p> must be 3 to 250 char long',
            })

        return errors

    @staticmethod
    def validate_get_all(query_params):
        errors = []

        # limit validation
        try:
            if 'limit' in query_params:
                int(query_params['limit'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'limit',
                'message': '<limit> must be present in query parameters and be numeric'
            })

        # offset validation
        try:
            if 'offset' in query_params:
                int(query_params['offset'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'offset',
                'message': '<offset> must be present in query parameters and be numeric'
            })

        return errors
