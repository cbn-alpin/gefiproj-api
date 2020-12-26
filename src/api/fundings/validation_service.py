ERROR_CODE = 'VALIDATION_ERROR'


class FundingValidationService:
    @staticmethod
    def validate_post(funding):
        errors = []
        
        # funding id validation
        try:
            if 'id_f' in funding:
                int(funding['id_f'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_f',
                'message': '<id_f> doit être un nombre',
            })

        # project id validation
        if 'id_p' not in funding:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'id_p',
                'message': 'Le champs <id_p> est manquant',
            })

        try:
            if 'id_p' in funding:
                int(funding['id_p'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_p',
                'message': '<id_p> doit être un nombre',
            })

        # funder id validation
        if 'id_financeur' not in funding:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'id_financeur',
                'message': 'Le champs <id_financeur> est manquant',
            })
            
        try:
            if 'id_financeur' in funding:
                int(funding['id_financeur'])
        except ValueError:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'id_financeur',
                'message': '<id_financeur> doit être un nombre',
            })
            
        # montant_arrete_f validation
        if 'montant_arrete_f' not in funding:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'montant_arrete_f',
                'message': 'Le champs <montant_arrete_f> est manquant',
            })

        # statut validation
        if 'statut_f' not in funding:
            errors.append({
                'code': ERROR_CODE,
                'type': 'MISSING_PARAMETER',
                'field': 'statut_f',
                'message': 'Le champs <statut_f> est manquant',
            })

        if 'statut_f' in funding and funding['statut_f'] not in ["ANTR", "ATR", "SOLDE"]:
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'statut_f',
                'message': 'La valeur du champs <statut_f> doit être soit <ANTR>, <SOLDE> ou <ATR>',
            })
            
        if 'statut_f' in funding and funding['statut_f'] == 'SOLDE' and \
            ( any(key not in funding for key in ['montant_arrete_f','id_financeur','statut_f','date_solde_f']) or \
            (funding['montant_arrete_f'] == None or
            funding['id_financeur'] == None or
            funding['statut_f'] == None or
            funding['date_solde_f'] == None ) ):
            errors.append({
                'code': ERROR_CODE,
                'type': 'VALUE_ERROR',
                'field': 'statut_f',
                'message': 'Le statut du financement ne peut pas être soldé.',
            })

        return errors
