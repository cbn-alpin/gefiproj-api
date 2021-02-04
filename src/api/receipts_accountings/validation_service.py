from src.shared.data_validation_utils import DataValidationUtils

class ReceiptAccountingValidationService:
    @staticmethod
    def validate_post(receipt_accounting_data):
        receipt_keys = ['montant_rc', 'annee_rc']
        errors = DataValidationUtils.check_keys(receipt_keys, receipt_accounting_data)

        errors = DataValidationUtils.check_int_value('annee_rc', receipt_accounting_data, errors)
        errors = DataValidationUtils.check_float_montant('montant_rc', receipt_accounting_data, errors)

        return errors
