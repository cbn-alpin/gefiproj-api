from src.shared.data_validation_utils import DataValidationUtils

ERROR_CODE = 'VALIDATION_ERROR'


class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt_data):
        receipt_keys = ['id_f', 'montant_r', 'annee_r']
        errors = DataValidationUtils.check_keys(receipt_keys, receipt_data)

        errors = DataValidationUtils.check_int_value('id_f', receipt_data, errors)
        errors = DataValidationUtils.check_int_value('annee_r', receipt_data, errors)
        errors = DataValidationUtils.check_float_montant('montant_r', receipt_data, errors)

        return errors


class InputOutputValidationService:
    @staticmethod
    def validate_post(input_output_data):
        input_output_keys = ['annee_recette_es', 'annee_affectation_es', 'montant_es']
        errors = DataValidationUtils.check_keys(input_output_keys, input_output_data)

        errors = DataValidationUtils.check_int_value('annee_recette_es', input_output_data, errors)
        errors = DataValidationUtils.check_int_value('annee_affectation_es', input_output_data, errors)
        errors = DataValidationUtils.check_input_output_montant('montant_es', input_output_data, errors)

        return errors
