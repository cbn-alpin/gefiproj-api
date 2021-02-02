from src.shared.data_validation_utils import DataValidationUtils, ERROR_CODE


class ExportValidationService:
    @staticmethod
    def validate(export_params_data):
        export_params_keys = ['version', 'annee_ref', 'partages']

        errors = DataValidationUtils.check_keys(export_params_keys, export_params_data)

        errors = DataValidationUtils.check_int_value('version', export_params_data, errors)
        errors = DataValidationUtils.check_int_value('annee_ref', export_params_data, errors)
        errors = DataValidationUtils.check_list('partages', export_params_data, errors)

        if 'version' in export_params_data:
            if export_params_data['version'] != 1 and export_params_data['version'] != 2:
                errors.append({
                    'code': ERROR_CODE,
                    'type': 'VALUE_ERROR',
                    'field': 'version',
                    'message': '<version> must be either 1 or 2.',
                })

            # annee_max is mandatory when version is 2
            if export_params_data['version'] == 2:
                errors = errors + DataValidationUtils.check_keys(['annee_max'], export_params_data)
                errors = DataValidationUtils.check_int_value('annee_max', export_params_data, errors)

        if 'entete' in export_params_data:
            errors = DataValidationUtils.check_list('entete', export_params_data, errors)

        if 'partages' in export_params_data:
            shares = export_params_data['partages']
            for it in shares:
                # TODO: Check email validity
                errors = errors + DataValidationUtils.check_keys(['email', 'type', 'permission'], it)

        return errors
