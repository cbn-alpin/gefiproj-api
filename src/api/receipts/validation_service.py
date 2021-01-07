from src.api.users.validation_service import UserValidationService

ERROR_CODE = 'VALIDATION_ERROR'


class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt_data):
        receipt_keys = ['id_f', 'montant_r', 'annee_r']
        errors = UserValidationService.check_keys(receipt_keys, receipt_data)

        try:
            if 'id_f' in receipt_data:
                receipt_data['id_f'] = int(receipt_data['id_f'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_f',
                'message': '<id_f> must be a number. Ex: 3',
            })

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

        try:
            if 'annee_r' in receipt_data:
                receipt_data['annee_r'] = int(receipt_data['annee_r'])
                if receipt_data['annee_r'] < 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'annee_r',
                'message': '<annee_r> must be a year. Ex: 2021',
            })

        return errors
