from datetime import datetime
import json
from flask import Blueprint, current_app, jsonify, request, Response
from shared.entity import Session
from ..fundings.entities import Funding, FundingSchema
from .entities import Receipt, ReceiptSchema


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.',404)


    @staticmethod
    def get_receipt_by_funding(funding_id: int):
        response = Response()
        try:
            session = Session()  
            receipt_object = session.query(Receipt).filter_by(id_f=funding_id).all()

            # Transforming into JSON-serializable objects
            schema = ReceiptSchema(many=True)
            receipt = schema.dump(receipt_object)
            # Serializing as JSON
            session.close()
            print('here 2')
            response = jsonify(receipt)
            print('here 4')
        except ValueError as error:
            response.data = str(error.args[0])
            response.status_code = error.args[1]
        finally:  
            return response