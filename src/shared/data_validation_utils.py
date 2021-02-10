ERROR_CODE = 'VALIDATION_ERROR'


class DataValidationUtils:
    @staticmethod
    def check_keys(keys: [], user):
        errors = []

        for key in keys:
            if key not in user:
                errors.append({
                    'code': ERROR_CODE,
                    'type': 'MISSING_PARAMETER',
                    'field': key,
                    'message': 'Paramter <{}> is missing'.format(key),
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
                'message': f'<{key}> must be a number. Ex: 3',
            })
        return err

    @staticmethod
    def check_float_montant(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                data[key] = float(data[key])
                if data[key] < 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> must be a positive double precision number. Ex: 173.59',
            })

        return err

    @staticmethod
    def check_input_output_montant(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                data[key] = float(data[key])
                if data[key] == 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> must be a double precision number != 0. Ex: 173.59 or -89.23',
            })

        return err

    @staticmethod
    def check_list(key: str, data, errors: []):
        err = errors
        try:
            if key in data and type(data[key]) is not list:
                raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> must be a list.',
            })
        return err

    @staticmethod
    def check_string_value(key: str, data, errors: []):
        err = errors
        try:
            if key in data:
                data[key] = str(data[key])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': key,
                'message': f'<{key}> must be a positive double precision number. Ex: 173.59',
            })

        return err
