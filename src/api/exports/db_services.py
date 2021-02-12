from flask import current_app

from src.shared.entity import Session


class ExportDBService:
    @staticmethod
    def get_suivi_financement(version, annee_ref, annee_max=0):
        session = None

        try:
            session = Session()
            result = session.execute("select * from suivi_financement(:version, :annee_ref, :annee_max)",
                                     {'version': version, 'annee_ref': annee_ref, 'annee_max': annee_max})
            return result
        except Exception as se:
            current_app.logger.error(se, exc_info=True)
            return None
        finally:
            if session:
                session.close()

    @staticmethod
    def get_bilan_financier(annee_ref):
        session = None

        try:
            session = Session()
            result = session.execute("select * from bilan_financier(:annee_ref) ORDER BY annee_recette",
                                     {'annee_ref': annee_ref}
                                     )
            return result
        except Exception as se:
            current_app.logger.error(se, exc_info=True)
            return None
        finally:
            if session:
                session.close()

    @staticmethod
    def get_bilan_financier_recettes_comptables(annee_ref):
        session = None

        try:
            session = Session()
            result = session.execute("select montant_rc from recette_comptable where annee_rc=:annee_ref",
                                     {'annee_ref': annee_ref}
                                     )
            montant_d = None
            for r in result:
                montant_d = r['montant_d']
                if montant_d:
                    return 0
                else:
                    return montant_d

        except Exception as se:
            current_app.logger.error(se, exc_info=True)
            return None
        finally:
            if session:
                session.close()

    @staticmethod
    def get_bilan_financier_depenses(annee_ref):
        session = None

        try:
            session = Session()
            result = session.execute("select montant_d from depense where annee_d=:annee_ref",
                                     {'annee_ref': annee_ref}
                                     )
            return result
        except Exception as se:
            current_app.logger.error(se, exc_info=True)
            return None
        finally:
            if session:
                session.close()
