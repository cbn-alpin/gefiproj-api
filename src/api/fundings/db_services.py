from datetime import datetime
import json
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import func, desc
from sqlalchemy.orm import join
from .entities import Funding, FundingSchema
from ..receipts.entities import Receipt, ReceiptSchema
from ..projects.entities import Project, ProjectSchema
from src.shared.entity import Session

STATUS_DEFAULT = 'ANTR'
STATUS_SOLDE = 'SOLDE'

class FundingDBService:
    @staticmethod
    def get_funding_by_project_id(project_id):
        session = Session()
        found_funding = session.query(Funding).filter_by(id_p=project_id).all()
        session.close()
        return found_funding


    @staticmethod
    def check_project_exists(project_id):
        session = Session()
        existing_project = session.query(Project).filter_by(id_p=project_id).first()
        session.close()
        
        if existing_project is None:
            raise ValueError(f'Le projet {project_id} n\'existe pas.',404)
    
    @staticmethod
    def check_have_receipt(funding_id):
        session = Session()
        existing_receipt = session.query(Receipt).filter_by(id_f=funding_id).first()
        session.close()
        
        if existing_receipt is not None:
            raise ValueError(f'Ce financement ne peut pas être supprimé car il possède des recettes.',405)
        
        
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.',404)


    @staticmethod
    def get_funding_by_project(project_id: int):
        session = Session()  
        funding_object = session.query(Funding).filter(Funding.id_p == project_id).order_by(Funding.id_f.desc()).all()
        # sum of receipts generated by this funding
        rest_amount_funding_object = session.query(Funding.id_f, (Funding.montant_arrete_f - func.sum(Receipt.montant_r)).label('difference')) \
            .join(Receipt, Receipt.id_f == Funding.id_f, isouter=True) \
            .filter(Funding.id_p == project_id)\
            .group_by(Funding.id_f)\
            .order_by(Funding.id_f.desc())

        # Transforming into JSON-serializable objects
        schema = FundingSchema(many=True)
        funding = schema.dump(funding_object)
        rest_amount_funding = schema.dump(rest_amount_funding_object)
            
        for i,f in enumerate(funding):
            if rest_amount_funding[i]['id_f'] == f['id_f']:
                if f['statut_f'] == STATUS_SOLDE:
                    f['solde'] = True
                else:
                    f['solde'] = False

                if rest_amount_funding[i]['difference'] == None:
                    f['difference'] = 0
                else:
                    f['difference'] = rest_amount_funding[i]['difference']

        # Serializing as JSON
        session.close()
        return funding


    @staticmethod
    def insert_funding(posted_funding):
        # Convert date format
        # posted_funding = convert_funding_dates(posted_funding)

        posted_funding['montant_arrete_f'] = float(posted_funding['montant_arrete_f'])
        # Mount funding object
        posted_funding = FundingSchema(only=(
            'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f', 'date_limite_solde_f',
            'commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f', 'imputation_f')) \
            .load(posted_funding)
        data = Funding(**posted_funding)

        # Persist funding
        session = Session()
        session.add(data)
        session.commit()

        # Return created funding
        new_funding = FundingSchema().dump(data)
        session.close()
        return new_funding


    @staticmethod
    def update_funding(funding):
        # Convert date format
        #data = convert_funding_dates(data)

        # Mount funding object
        funding = FundingSchema(only=(
            'id_f', 'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f',
            'date_limite_solde_f', 'commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f',
            'imputation_f')) \
            .load(funding)
        funding = Funding(**funding)
        # Start DB session
        session = Session()
        session.merge(funding)
        session.commit()

        # Return updated funding
        updated_funding = FundingSchema().dump(funding)
        session.close()
        return updated_funding


    @staticmethod
    def delete_funding(funding_id):
        session = Session()
        funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.delete(funding)
        session.commit()
        session.close()
        response = {
            'message': f'Le financement {funding_id} a été supprimé'
        }
        return response


    def convert_funding_dates(self,funding):
        if 'date_solde_f' in funding:
            funding['date_solde_f'] = date_convert(funding['date_solde_f'])
        else:
            funding['date_solde_f'] = None

        if 'date_arrete_f' in funding:
            funding['date_arrete_f'] = date_convert(funding['date_arrete_f'])
        else:
            funding['date_arrete_f'] = None

        if 'date_limite_solde_f' in funding:
            funding['date_limite_solde_f'] = date_convert(funding['date_limite_solde_f'])
        else:
            funding['date_limite_solde_f'] = None
        return funding


    def date_convert(self,date_time_str):
        date = None
        if date_time_str is not None:
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
            date = date_time_obj.date().isoformat()
        return date
