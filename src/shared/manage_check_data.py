from .manage_error import ManageErrorUtils, CodeError, TError
import re
import datetime

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
    def check_format_value(key: str, data, typeV: int or float or str or bool, name: str):
        try:
            if key in data and ( \
                (typeV != float and isinstance(data[key], typeV) == False)  or \
                (typeV == float and ( isinstance(data[key], int) == False and isinstance(data[key], float) == False ) )):
                message = "Erreur de format du champs '{}'".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
    
    @staticmethod
    def check_format_array(key: str, data, size: int, name: str):
        try:
            if key in data and (len(data[key]) <= 0 or len(data[key]) > size) and isinstance(data[key], type(list)) == False:
                message = "Erreur de format du champs '{}'".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
        
    @staticmethod
    def check_format_date(key: str, data, name: str):
        try:
            if key in data and data[key] is not None:
                datetime.datetime.strptime(data[key], '%Y-%m-%d').date()
        except ValueError as error:
            message = "Erreur de format du champs '{}'".format(name)
            ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
            raise

    @staticmethod
    def check_format_mail(key: str, data, name: str):
        try:
            if key in data and not re.search(EMAIL_REGEX, data[key]):
                message = "Erreur de format du champs '{}'".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_array_is_subset(key: str, arrayA: list, arrayB: list, name: str):
        try:
            if arrayA is not None and arrayB is not None and set(arrayA).issubset(set(arrayB)) == False:
                message = "Erreur de la valeur du champs '{}'".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
    
    @staticmethod
    def check_not_none(key: str, data, name: str):
        try:
            if key in data and (data[key] is None or data[key] <= 0):
                message = "Le champs '{}' est vide".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_string_lenght(key: str, data, name: str, limitInf: int, limitSup: int = None):
        try:
            if limitSup is None and key in data and len(data[key]) < limitInf:
                message = "Erreur sur la longueur du champs '{}'. Il doit avoir au moins {} caractères.".format(name,limitInf)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
            elif limitSup is not None and key in data and (len(data[key]) < limitInf or len(data[key]) > limitSup):
                message = "Erreur sur la longueur du champs '{}'. Il doit avoir entre {} et {} caractères".format(name, limitInf, limitSup)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_duplicate_value(key: str, data, name: str):
        try:
            if key in data and len(data[key]) > 0 and len(data[key]) != len(set(data[key])):
                message = "Erreur de duplication de la valeur sur le champs '{}'".format(name)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.DUPLICATION_VALUE_ERROR, message, 422)
        except ValueError as error:
            raise

    @staticmethod
    def check_date_is_after_another(keyBef: str, keyAft:str, data, nameKBef:str, nameKAft: str):
        try:
            if keyBef in data and keyAft in data and \
                data[keyBef] != None and data[keyAft] != None and \
                datetime.datetime.strptime(data[keyBef], '%Y-%m-%d').date() > datetime.datetime.strptime(data[keyAft], '%Y-%m-%d').date():
                message = "format date non respecté : la {} doit être postérieure à la {}.".format(nameKBef,nameKAft)
                ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            raise
        