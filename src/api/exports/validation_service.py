from src.shared.data_validation_utils import DataValidationUtils


class ExportValidationService:
    @staticmethod
    def validate_v1(export_params_data):
        export_params_keys = ['annee_ref', 'partages']

        errors = DataValidationUtils.check_keys(export_params_keys, export_params_data)

        errors = DataValidationUtils.check_int_value('annee_ref', export_params_data, errors)
        errors = DataValidationUtils.check_list('partages', export_params_data, errors)

        if 'entete' in export_params_data:
            errors = DataValidationUtils.check_list('entete', export_params_data, errors)

        if 'partages' in export_params_data:
            shares = export_params_data['partages']
            for it in shares:
                # TODO: Check email validity
                errors = DataValidationUtils.check_keys(['email', 'type', 'permission'], it)

        return errors
