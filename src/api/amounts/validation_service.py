from src.shared.manage_check_data import ManageCheckDataUtils
from flask import current_app

KEYS = ['montant_ma', 'annee_ma', 'id_r']


class AmountValidationService:
    @staticmethod
    def validate(amount):
        try:
            amount_keys = KEYS
            ManageCheckDataUtils.check_keys(amount_keys, amount)
            
            ManageCheckDataUtils.check_format_value('annee_ma', amount, int, 'année du montant affecté')
            ManageCheckDataUtils.check_format_value('montant_ma', amount, float, 'montant du montant affecté')
            ManageCheckDataUtils.check_format_value('id_r', amount, int, 'id de la recette')
        
            ManageCheckDataUtils.check_not_none('annee_ma', amount, 'année du montant affecté')
            ManageCheckDataUtils.check_not_none('montant_ma', amount, 'montant du montant affecté')
            ManageCheckDataUtils.check_not_none('id_r', amount, 'id de la recette')
        except ValueError as error:
            current_app.logger.error(f"AmountValidationService - validate : {error}")
            raise