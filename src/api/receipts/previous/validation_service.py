from flask import current_app

from src.shared.manage_check_data import ManageCheckDataUtils
from src.shared.manage_error import ManageErrorUtils, CodeError, TError

KEYS = ['annee_recette_es', 'annee_affectation_es', 'montant_es']


class InputOutputValidationService:
    @staticmethod
    def validate_post(input_output_data):
        try:
            input_output_keys = KEYS
            # validation keys
            ManageCheckDataUtils.check_keys(input_output_keys, input_output_data)
            # validation format
            ManageCheckDataUtils.check_format_value('annee_recette_es', input_output_data, int,
                                                    "année recette de l'entrée sortie")
            ManageCheckDataUtils.check_format_value('annee_affectation_es', input_output_data, int,
                                                    "année affectation de l'entrée sortie")
            ManageCheckDataUtils.check_format_value('montant_es', input_output_data, float,
                                                    "montant de l'entrée sortie")
            if "montant_es" in input_output_data:
                input_output_data["montant_es"] = float(input_output_data["montant_es"])
                if input_output_data["montant_es"] == 0:
                    message = "montant_es must be a double precision number != 0. Ex: 173.59 or -89.23"
                    ManageErrorUtils.value_error(CodeError.VALIDATION_ERROR, TError.VALUE_ERROR, message, 422)
        except ValueError as error:
            current_app.logger.error(f"InputOutputValidationService - validate_post : {error}")
            raise
