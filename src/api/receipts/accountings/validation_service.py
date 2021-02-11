from flask import current_app

from src.shared.manage_check_data import ManageCheckDataUtils


class ReceiptAccountingValidationService:
    @staticmethod
    def validate_post(receipt_accounting_data):
        try:
            receipt_keys = ['montant_rc', 'annee_rc']
            ManageCheckDataUtils.check_keys(receipt_keys, receipt_accounting_data)

            ManageCheckDataUtils.check_format_value('annee_rc', receipt_accounting_data, int, "année recette")
            ManageCheckDataUtils.check_format_value('montant_rc', receipt_accounting_data, float, "montant recette")
        except ValueError as error:
            current_app.logger.warning(error)
            raise
