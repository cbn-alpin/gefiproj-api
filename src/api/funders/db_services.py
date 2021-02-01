from flask import Blueprint, current_app
from src.shared.entity import Session
from .entities import Funder, FunderSchema
from ..fundings.entities import Funding

class FunderDBService:
    @staticmethod
    def get_all_funders():
        session = Session()  
        funder_object = session.query(Funder).order_by(Funder.nom_financeur).all()
        # Transforming into JSON-serializable objects
        schema = FunderSchema(many=True)
        funders = schema.dump(funder_object)
        # Serializing as JSON
        session.close()
        return funders
            
    @staticmethod
    def insert(funder):
        posted_funder = FunderSchema(only=('nom_financeur', 'ref_arret_attributif_financeur')).load(funder)
        data = Funder(**posted_funder)
        
        session = Session()
        session.add(data)
        session.commit()

        inserted_Funder = FunderSchema().dump(data)
        session.close()
        return inserted_Funder


    @staticmethod
    def update(funder):
        update_funder = FunderSchema(only=('id_financeur', 'nom_financeur', 'ref_arret_attributif_financeur')).load(funder)
        data = Funder(**update_funder)
        
        session = Session()
        session.merge(data)
        session.commit()

        updated_funder = FunderSchema().dump(data)
        session.close()
        return updated_funder
    
    @staticmethod
    def delete(funder_id: int):
        session = Session()
        funder = session.query(Funder).filter_by(id_financeur=funder_id).first()
        session.delete(funder)
        session.commit()
        session.close()
        response = {
            'message': f'Le financeur {funder.nom_financeur} a été supprimé'
        }
        return response
    
    @staticmethod
    def check_funder_use_in_funding(funder_id: int):
        session = Session()  
        funder = session.query(Funder).filter_by(id_financeur=funder_id).all()
        funding = session.query(Funding).filter(Funding.id_financeur==funder_id).all()
        session.close()
        
        if funding is not None and len(funding) > 0:
            raise ValueError(f'Le financeur {funder.nom_financeur} est affecté à len(funding) financement(s)',404)
