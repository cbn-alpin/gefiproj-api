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
