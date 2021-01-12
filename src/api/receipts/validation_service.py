from src.api.users.validation_service import UserValidationService

ERROR_CODE = 'VALIDATION_ERROR'


class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt_data):
        receipt_keys = ['id_f', 'montant_r', 'annee_r']
        errors = UserValidationService.check_keys(receipt_keys, receipt_data)

        errors = UserValidationService.check_int_value('id_f', receipt_data, errors)
        errors = UserValidationService.check_int_value('annee_r', receipt_data, errors)
        errors = UserValidationService.check_float_montant('montant_r', receipt_data, errors)

        return errors
