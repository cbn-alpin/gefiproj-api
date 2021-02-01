ERROR_CODE = 'VALIDATION_ERROR'


class FunderValidationService:
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
            else:
                raise ValueError
        except ValueError:
            err.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> doit être défini et doit être un nombre entier.',
            })
        return err

    @staticmethod
    def check_string_value(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                data[key] = str(data[key])
            else:
                raise ValueError
        except ValueError:
            err.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> doit être défini et doit être au moins un caractère.',
            })
        return err


    @staticmethod
    def validate_post(funder_data):
        financeur_keys = ['nom_financeur', 'ref_arret_attributif_financeur']
        errors = FunderValidationService.check_keys(financeur_keys, funder_data)

        errors = FunderValidationService.check_string_value('nom_financeur', funder_data, errors)
        errors = FunderValidationService.check_string_value('ref_arret_attributif_financeur', funder_data, errors)
        return errors
    