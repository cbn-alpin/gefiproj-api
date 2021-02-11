from flask import current_app
from src.shared.manage_check_data import ManageCheckDataUtils

KEYS = ['id_f', 'montant_r', 'annee_r']

class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt):
        try:
            receipt_keys = KEYS
            # validation keys
            ManageCheckDataUtils.check_keys(receipt_keys, receipt)
            
            ManageCheckDataUtils.check_format_value('id_f', receipt, int, 'id du financement')
            ManageCheckDataUtils.check_format_value('annee_r', receipt, int, 'année de la recette')
            ManageCheckDataUtils.check_format_value('montant_r', receipt, float, 'montant de la recette')
            
            ManageCheckDataUtils.check_not_none('annee_r', receipt, 'année de la recette')
            ManageCheckDataUtils.check_not_none('montant_r', receipt, 'montant de la recette')
            ManageCheckDataUtils.check_not_none('id_f', receipt, 'id du financement')
        except ValueError as error:
            current_app.logger.warning(error)
            raise
