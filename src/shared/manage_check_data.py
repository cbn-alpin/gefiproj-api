from .manage_error import ManageErrorUtils, CodeError, TError
import re

EMAIL_REGEX = '^[a-z0-9A-Z._%+-]+[@]\w+[.]\w{2,3}$'


class ManageCheckDataUtils:
    @staticmethod
    def check_keys(keys: [], obj):
        try:
            if all(name in obj for name in keys) == False:
                message = "Champs Manquants : " + ", ".join([name for name in keys if name not in obj])
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.MISSING_PARAMETER, message, 422)
        except ValueError as error:
            raise
    
    @staticmethod
    def check_format_value(key: str, data, typeV: int or float or str or bool):
        try:
            if key in data and isinstance(data[key], typeV) == False:
                message = "Erreur de format du champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
    
    @staticmethod
    def check_format_array(key: str, data, typeV: list, size: int):
        try:
            if key in data and (len(data[key]) <= 0 or len(data[key]) > size) and isinstance(data[key], type(typeV)) == False:
                message = "Erreur de format du champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_format_mail(key: str, data):
        try:
            if key in data and not re.search(EMAIL_REGEX, data[key]):
                message = "Erreur de format du champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_array_is_subset(key: str, arrayA: list, arrayB: list):
        try:
            if arrayA is not None and arrayB is not None and set(arrayA).issubset(set(arrayB)) == False:
                message = "Erreur de la valeur du champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_string_inf_lenght(key: str, data, size: int):
        try:
            if key in data and len(data[key]) < size:
                message = "Erreur de la longueur du champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_duplicate_value(key: str, data):
        try:
            if key in data and len(data[key]) > 0 and len(data[key]) != len(set(data[key])):
                message = "Erreur de duplication de la valeur sur le champs {}".format(key)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.DUPLICATION_VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
