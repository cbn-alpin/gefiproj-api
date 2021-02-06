ERROR_CODE = "VALIDATION_ERROR"
from src.shared.data_validation_utils import DataValidationUtils


class FunderValidationService:
    @staticmethod
    def validate_post(funder_data):
        financeur_keys = ['nom_financeur']
        errors = DataValidationUtils.check_keys(financeur_keys, funder_data)

        errors = DataValidationUtils.check_string_value('nom_financeur', funder_data, errors)
        return errors
    