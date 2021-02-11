from flask import current_app

from src.shared.manage_check_data import ManageCheckDataUtils


class ReceiptValidationService:
    @staticmethod
    def validate_post(receipt_data):
        try:
            receipt_keys = ['id_f', 'montant_r', 'annee_r']
            # validation keys
            ManageCheckDataUtils.check_keys(receipt_keys, receipt_data)
            ManageCheckDataUtils.check_format_value('id_f', receipt_data, int, 'id_f')
            ManageCheckDataUtils.check_format_value('annee_r', receipt_data, int, 'annee_r')
            ManageCheckDataUtils.check_format_value('montant_r', receipt_data, float, 'montant_r')

        except ValueError as error:
            current_app.logger.warning(error)
            raise
