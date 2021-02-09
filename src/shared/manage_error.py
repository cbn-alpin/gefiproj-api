from enum import Enum
from jwt.exceptions import ExpiredSignatureError

class CodeError(Enum):
    VALIDATION_ERROR = 'VALIDATION_ERROR',
    DB_VALIDATION_WARNING = 'DB_VALIDATION_WARNING',
    DB_VALIDATION_ERROR = "DB_VALIDATION_ERROR",
    DB_VALUE_REFERENCED = 'DB_VALUE_REFERENCED',
    DB_DELETE_ERROR = 'DB_DELETE_ERROR',
    TOKEN_HAS_NOT_ENOUGH_PRIVILEGES = 'TOKEN_HAS_NOT_ENOUGH_PRIVILEGES',
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR",
    LOGOUT_ERROR = "LOGOUT_ERROR",
    REGISTER_ERROR = "REGISTER_ERROR",
    TOKEN_REVOKED_ERROR = "TOKEN_REVOKED_ERROR",
    TOKEN_EXPIRED = "TOKEN_EXPIRED",
    TOKEN_REQUIRED = "TOKEN_REQUIRED",
    NOT_PERMISSION = "NOT_PERMISSION"


class TError(Enum):
    MISSING_PARAMETER = 'MISSING_PARAMETER',
    VALUE_ERROR = 'VALUE_ERROR',
    TOKEN_ERROR = 'TOKEN_ERROR',
    DUPLICATION_VALUE_ERROR = 'DUPLICATION_VALUE_ERROR',
    UNIQUE_CONSTRAINT_ERROR = 'UNIQUE_CONSTRAINT_VALUE_ERROR',
    DATA_NOT_FOUND = 'DATA_NOT_FOUND',
    WRONG_AUTHENTICATION = "WRONG_AUTHENTICATION",
    REGISTER = "REGISTER_ERROR",
    UPDATE_ERROR = "UPDATE_ERROR",
    INSERT_ERROR = "INSERT_ERROR",
    DELETE_ERROR = "DELETE_ERROR",
    INACTIVE_ACCOUNT = "INACTIVE_ACCOUNT",
    LOGOUT = "LOGOUT",
    ANY_TYPE_ERROR = ''


class ManageErrorUtils:
    @staticmethod
    def value_error(code: CodeError, type: TError, msg: str, code_return: int):
        msg = {
            'code': code.value,
            'type': type.value,
            'message': str(msg),
        }
        raise ValueError(msg, code_return)

    @staticmethod
    def exception(code: CodeError, type: TError, msg: str, code_return: int):
        msg = {
        'code': code.value,
        'type': type.value,
        'message': str(msg),
        }
        raise Exception(msg, code_return)
