from enum import Enum

class CodeError(Enum):
    VALIDATION_ERROR = 'VALIDATION_ERROR',
    DATA_NOT_FOUND = 'DATA_NOT_FOUND',
    UNIQUE_CONSTRAINT_ERROR = 'UNIQUE_CONSTRAINT_VALUE_ERROR'


class TError(Enum):
    MISSING_PARAMETER = 'MISSING_PARAMETER',
    VALUE_ERROR = 'VALUE_ERROR',
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
