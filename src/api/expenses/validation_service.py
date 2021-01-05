from src.api.projects.validation_service import ERROR_CODE
from src.api.users.validation_service import UserValidationService


class ExpenseValidationService:
    @staticmethod
    def validate_post(expense_data):
        expense_keys = ['annee_d', 'montant_d']
        # TODO: make check_keys() independent of UserValidationService
        errors = UserValidationService.check_keys(expense_keys, expense_data)

        try:
            # TODO check minimum and maximum year values of validity
            if 'annee_d' in expense_data:
                expense_data['annee_d'] = int(expense_data['annee_d'])
                if expense_data['annee_d'] < 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'annee_d',
                'message': '<annee_d> must be a year. Ex: 2021',
            })

        try:
            if 'montant_d' in expense_data:
                expense_data['montant_d'] = float(expense_data['montant_d'])
                if expense_data['montant_d'] < 0:
                    raise ValueError
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'montant_d',
                'message': '<montant_d> must be a positive double precision number. Ex: 173.59',
            })

        return errors