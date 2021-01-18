from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from src.shared.entity import Session
from sqlalchemy import func, desc
from sqlalchemy.orm import join
from .entities import Funder, FunderSchema

resources = Blueprint('funders', __name__)


@resources.route('/api/funders', methods=['GET'])
def get_funders():
    current_app.logger.debug('In GET /api/funders')

    session = Session()  
    funder_object = session.query(Funder).order_by(Funder.nom_financeur).all()

    # Transforming into JSON-serializable objects
    schema = FunderSchema(many=True)
    funders = schema.dump(funder_object)

    # Serializing as JSON
    session.close()
    return jsonify(funders)
