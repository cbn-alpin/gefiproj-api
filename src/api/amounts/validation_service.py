from src.api.users.validation_service import UserValidationService

ERROR_CODE = 'VALIDATION_ERROR'


class AmountValidationService:
    @staticmethod
    def validate_post(amount_data):
        amount_keys = ['id_r', 'montant_ma', 'annee_ma']
        errors = UserValidationService.check_keys(amount_keys, amount_data)

        errors = UserValidationService.check_int_value('id_r', amount_data, errors)
        errors = UserValidationService.check_float_montant('montant_ma', amount_data, errors)
        errors = UserValidationService.check_int_value('annee_ma', amount_data, errors)

        return errors
