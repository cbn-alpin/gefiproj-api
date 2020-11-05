from flask import Blueprint, current_app, jsonify, request
from shared.auth import AuthError
from shared.entity import Session

from .entities import Financement, FinancementSchema

from datetime import datetime
# Versions infos

resources = Blueprint('financements', __name__)


@resources.route('/financements', methods=['GET'])
def get_all_financement():
    current_app.logger.info('In GET /financements')
    # Fetching from the database
    session = Session()
    financements_objects = session.query(Financement).all()

    # Transforming into JSON-serializable objects
    schema = FinancementSchema(many=True)
    financements = schema.dump(financements_objects)

    # Serializing as JSON
    session.close()
    return jsonify(financements)


@resources.route('/financements/<int:descId>', methods=['GET'])
def get_financements_by_project(descId):
    # Checks
    check_financement_exists

    session = Session()
    financement_object = session.query(Financement).filter_by(id_p=descId).all()

    # Transforming into JSON-serializable objects
    schema = FinancementSchema(many=True)
    financement = schema.dump(financement_object)

    # Serializing as JSON
    session.close()
    return jsonify(financement)


@resources.route('/financements', methods=['POST'])
# @requires_auth
def add_financement():
    body = request.get_json()
    # Convert date format
    if 'date_solde_f' in body: 
        body['date_solde_f'] = date_convert(body['date_solde_f'])
    if 'date_arrete_f' in body: 
        body['date_arrete_f'] = date_convert(body['date_arrete_f']) 
    if 'date_limite_solde_f' in body: 
        body['date_limite_solde_f'] = date_convert(body['date_limite_solde_f'])
    # Init statut financement
    if 'statut_f' not in body: 
        body['statut_f'] = 'ANTR'

    # Mount financement object
    current_app.logger.debug('In POST /financements')
    posted_desc = FinancementSchema(only=('id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f', 'date_limite_solde_f','commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f', 'imputation_f')) \
        .load(body)
    desc = Financement(**posted_desc)

    # Persist financement
    session = Session()
    session.add(desc)
    session.commit()

    # Return created financement
    new_desc = FinancementSchema().dump(desc)
    session.close()
    return jsonify(new_desc), 201


@resources.route('/financements/<int:descId>', methods=['PUT'])
# @requires_auth
def update_financement(descId):
    current_app.logger.debug('In PUT /financements/<int:descId>')

    # Load data
    data = dict(request.get_json())
    if 'id_f' not in data:
        data['id_f'] = descId

    # Checks
    check_financement_exists(data['id_f'])

    # Convert date format
    if 'date_solde_f' in data: 
        data['date_solde_f'] = date_convert(data['date_solde_f'])
    if 'date_arrete_f' in data: 
        data['date_arrete_f'] = date_convert(data['date_arrete_f']) 
    if 'date_limite_solde_f' in data: 
        data['date_limite_solde_f'] = date_convert(data['date_limite_solde_f'])

    # Mount financement object
    data = FinancementSchema(only=('id_f', 'id_p', 'id_financeur', 'montant_arrete_f', 'statut_f', 'date_solde_f', 'date_arrete_f', 'date_limite_solde_f','commentaire_admin_f', 'commentaire_resp_f', 'numero_titre_f', 'annee_titre_f', 'imputation_f')) \
        .load(data)
    financement = Financement(**data)

    # Start DB session
    session = Session()
    session.merge(financement)
    session.commit()

    # Return updated financement
    updated_desc = FinancementSchema().dump(financement)
    session.close()
    return jsonify(updated_desc), 200


@resources.route('/financements/<descId>', methods=['DELETE'])
# @requires_role('admin')
def delete_financements(descId):
    check_financement_exists(descId)

    session = Session()
    financement = session.query(Financement).filter_by(id_f=descId).first()
    session.delete(financement)
    session.commit()
    session.close()
    return '', 204


def check_financement_exists(descId):
    try:
        session = Session()
        existing_desc = session.query(Financement).filter_by(id_f=descId).first()
        session.close()
        if (existing_desc == None):
            raise ValueError('This financement does not exist')
    except ValueError:
        resp = jsonify({"error": {
            'code': 'FINANCEMENT_NOT_FOUND',
            'message': f'Financement with id {descId} does not exist.'
        }})
        resp.status_code = 404
        return resp


@resources.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def date_convert(date_time_str):
    ##### date_time_str : "2018-06-29 08:15:27.243860"
    date = None
    if date_time_str != None:
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')  
        date = date_time_obj.date().isoformat()
    return date
