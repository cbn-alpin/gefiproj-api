from shared.entity import Session

from ..fundings.entities import Funding


class FundingDBService:
    @staticmethod
    def get_funding_by_project_id(project_id):
        session = Session()
        found_funding = session.query(Funding).filter_by(id_p=project_id).all()
        session.close()
        return found_funding
