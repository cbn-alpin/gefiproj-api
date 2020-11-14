from shared.entity import Session

from ..financements.entities import Financement


class FinancementDBService:
    @staticmethod
    def get_financements_by_projet_id(projet_id):
        session = Session()
        fin_found = session.query(Financement).filter_by(id_p=projet_id).all()
        session.close()
        return fin_found
