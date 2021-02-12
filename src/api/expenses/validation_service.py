from src.shared.manage_check_data import ManageCheckDataUtils
from flask import current_app

KEYS = ['annee_d', 'montant_d']


class ExpenseValidationService:
    @staticmethod
    def validate(expense):
        try:
            expense_keys = KEYS
            ManageCheckDataUtils.check_keys(expense_keys, expense)
            
            ManageCheckDataUtils.check_format_value('annee_d', expense, int, 'année de la dépense')
            ManageCheckDataUtils.check_format_value('montant_d', expense, float, 'montant de la dépense')
            ManageCheckDataUtils.check_not_none('annee_d', expense, 'année de la dépense')
            ManageCheckDataUtils.check_not_none('montant_d', expense, 'montant de la dépense')
        except ValueError as error:
            current_app.logger.error(f"ExpenseValidationService - validate : {error}")
            raise

