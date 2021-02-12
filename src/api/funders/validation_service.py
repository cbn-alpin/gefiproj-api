from src.shared.manage_check_data import ManageCheckDataUtils
from flask import current_app

KEYS = ['nom_financeur']


class FunderValidationService:
    @staticmethod
    def validate(funder):
        try:
            financeur_keys = KEYS
            ManageCheckDataUtils.check_keys(financeur_keys, funder)
            ManageCheckDataUtils.check_format_value('nom_financeur', funder, str, 'nom du financeur')
            ManageCheckDataUtils.check_string_lenght('nom_financeur', 'nom du financeur', funder, 2, 250)
        except ValueError as error:
            current_app.logger.error(f"FunderValidationService - validate : {error}")
            raise
