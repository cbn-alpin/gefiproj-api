ERROR_CODE = 'VALIDATION_ERROR'


class AmountValidationService:
    @staticmethod
    def check_keys(keys: [], amount):
        errors = []

        for key in keys:
            if key not in amount:
                errors.append({
                    'code': ERROR_CODE,
                    'type': 'MISSING_PARAMETER',
                    'field': key,
                    'message': 'Le champs <{}> est manquant'.format(key),
                })
        return errors

    @staticmethod
    def check_int_value(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                data[key] = int(data[key])
        except ValueError:
            err.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> doit être un nombre entier.',
            })
        return err

    @staticmethod
    def check_float_montant(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                if float(data[key]) <= 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> doit être un nombre supérieur à 0.',
            })

        return err

    @staticmethod
    def validate_post(amount_data):
        amount_keys = ['id_r', 'montant_ma', 'annee_ma']
        errors = check_keys(amount_keys, amount_data)

        errors = check_int_value('id_r', amount_data, errors)
        errors = check_float_montant('montant_ma', amount_data, errors)
        errors = check_int_value('annee_ma', amount_data, errors)
        return errors
    