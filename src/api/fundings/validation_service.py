from src.shared.manage_check_data import ManageCheckDataUtils
from flask import current_app
from enum import Enum 

KEYS = ['id_p', 'id_financeur', 'montant_arrete_f', 'statut_f']
STATUS = ['ANTR', 'ATR', 'SOLDE']

class Status(Enum):
    ANTR = 'ANTR'
    ATR = 'ATR'
    SOLDE = 'SOLDE'
    
class FundingValidationService:
    @staticmethod
    def validate(funding):
        try:
            # validation keys
            if 'statut_f' in funding and funding['statut_f'] == Status.SOLDE.value:
                funding_solde_keys = KEYS
                funding_solde_keys.append('date_solde_f')
                ManageCheckDataUtils.check_keys(funding_solde_keys, funding)
                ManageCheckDataUtils.check_not_none('date_solde_f', funding, 'date de solde')
            else:
                funding_keys = KEYS
                ManageCheckDataUtils.check_keys(funding_keys, funding)
                
            # validation format
            ManageCheckDataUtils.check_format_value('id_p', funding, int, 'id projet')
            ManageCheckDataUtils.check_format_value('id_financeur', funding, int, 'id financeur')
            ManageCheckDataUtils.check_format_value('montant_arrete_f', funding, float, 'montant arrêté ou commande')
            ManageCheckDataUtils.check_format_value('statut_f', funding, str, 'statut')
            ManageCheckDataUtils.check_array_is_subset('statut_f', [funding['statut_f']], STATUS, 'statut')
            
            ManageCheckDataUtils.check_not_none('id_p', funding, 'id projet')
            ManageCheckDataUtils.check_not_none('id_financeur', funding, 'id financeur')
            ManageCheckDataUtils.check_not_none('montant_arrete_f', funding, 'montant arrêté ou commande')
            
            # Check date
            if 'date_arrete_f' in funding:
                ManageCheckDataUtils.check_format_date('date_arrete_f', funding, 'date arrêté ou commande')
            if 'date_solde_f' in funding:
                ManageCheckDataUtils.check_format_date('date_solde_f', funding, 'date de solde')
            if 'date_limite_solde_f' in funding:
                ManageCheckDataUtils.check_format_date('date_limite_solde_f', funding, 'date limite de solde')
                
            ManageCheckDataUtils.check_date_is_after_another('date_arrete_f', 'date_solde_f', funding, 'date arrêté ou commande', 'date de solde')
            ManageCheckDataUtils.check_date_is_after_another('date_arrete_f', 'date_limite_solde_f', funding, 'date arrêté ou commande', 'date limite de solde')
        except ValueError as error:
            current_app.logger.warning(error)
            raise
