from src.api.users.validation_service import UserValidationService

ERROR_CODE = 'VALIDATION_ERROR'


class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt_data):
        receipt_keys = ['id_f', 'montant_r', 'annee_r']
        errors = UserValidationService.check_keys(receipt_keys, receipt_data)

        errors = UserValidationService.check_int_value('id_f', receipt_data, errors)
        errors = UserValidationService.check_int_value('annee_r', receipt_data, errors)

        try:
            if 'montant_r' in receipt_data:
                receipt_data['montant_r'] = float(receipt_data['montant_r'])
                if receipt_data['montant_r'] < 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'montant_r',
                'message': '<montant_r> must be a positive double precision number. Ex: 173.59',
            })

        return errors
