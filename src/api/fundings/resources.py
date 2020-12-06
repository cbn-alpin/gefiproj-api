from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from src.shared.entity import Session
from .entities import Funding, FundingSchema

resources = Blueprint('funding', __name__)


@resources.route('/funding', methods=['GET'])
def get_all_fundings():
    current_app.logger.info('In GET /funding')
    # Fetching from the database
    session = Session()
    funding_objects = session.query(Funding).all()

    # Transforming into JSON-serializable objects
    schema = FundingSchema(many=True)
    fundings = schema.dump(funding_objects)

    # Serializing as JSON
    session.close()
    return jsonify(fundings)


@resources.route('/funding/<int:project_id>', methods=['GET'])
def get_fundings_by_project(project_id):
    current_app.logger.debug('In GET /funding/<int:project_id>')
    # Checks
    check_fuding_exists(project_id)

    session = Session()
    funding_object = session.query(Funding).filter_by(id_p=project_id).all()

    # Transforming into JSON-serializable objects
    schema = FundingSchema(many=True)
    funding = schema.dump(funding_object)

    # Serializing as JSON
    session.close()
    return jsonify(funding)


@resources.route('/funding', methods=['POST'])
# @requires_auth
def add_funding():
    current_app.logger.debug('In POST /funding')

    posted_funding = request.get_json()
    # Convert date format
    posted_funding = convert_funding_dates(posted_funding)
    # Init statut funding
    if 'statut_f' not in posted_funding:
        posted_funding['statut_f'] = 'ANTR'

    print('>>>>>>>>>>>>>>>>>>>>>')
    print(posted_funding)

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
    return jsonify(new_funding), 201


@resources.route('/funding/<int:funding_id>', methods=['PUT'])
# @requires_auth
def update_funding(funding_id):
    current_app.logger.debug('In PUT /funding/<int:funding_id>')

    # Load data
    data = request.get_json()
    if 'id_f' not in data:
        data['id_f'] = funding_id

    # Checks
    check_fuding_exists(data['id_f'])

    data = convert_funding_dates(data)

    # Mount funding object
    data = FundingSchema(only=(
        'id_f', 'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f',
        'date_limite_solde_f', 'commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f',
        'imputation_f')) \
        .load(data)
    funding = Funding(**data)

    # Start DB session
    session = Session()
    session.merge(funding)
    session.commit()

    # Return updated funding
    updated_funding = FundingSchema().dump(funding)
    session.close()
    return jsonify(updated_funding), 200


@resources.route('/funding/<int:funding_id>', methods=['DELETE'])
# @requires_role('admin')
def delete_funding(funding_id):
    check_fuding_exists(funding_id)

    session = Session()
    funding = session.query(Funding).filter_by(id_f=funding_id).first()
    session.delete(funding)
    session.commit()
    session.close()
    return '', 204


def check_fuding_exists(funding_id):
    try:
        session = Session()
        existing_desc = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_desc is None:
            raise ValueError('This funding does not exist')
    except ValueError:
        resp = jsonify({"error": {
            'code': 'FUNDING_NOT_FOUND',
            'message': f'Funding with id {funding_id} does not exist.'
        }})
        resp.status_code = 404
        return resp


def convert_funding_dates(funding):
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


def date_convert(date_time_str):
    # date_time_str : "2018-06-29 08:15:27.243860"
    date = None
    if date_time_str is not None:
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        date = date_time_obj.date().isoformat()
    return date
