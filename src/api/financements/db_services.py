from shared.entity import Session

from ..financements.entities import Financement


class FundingDBService:
    @staticmethod
    def get_funding_by_project_id(project_id):
        session = Session()
        fin_found = session.query(Financement).filter_by(id_p=project_id).all()
        session.close()
        return fin_found
