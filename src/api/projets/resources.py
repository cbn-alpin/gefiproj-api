from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from shared.entity import Session

from .entities import Projet, ProjetSchema
from ..users.resources import check_user_exists_by_id

resources = Blueprint('projets', __name__)


@resources.route('/projets', methods=['POST'])
@jwt_required
def add_projet():
    current_app.logger.debug('In POST /projets')
    posted_projet = ProjetSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u')) \
        .load(request.get_json())
    projet = Projet(**posted_projet)

    # check if user with id_u exists
    check_user_exists_by_id(projet.id_u)

    session = Session()
    session.add(projet)
    session.commit()

    new_projet = ProjetSchema().dump(projet)
    return jsonify(new_projet), 201


@resources.route('/projets', methods=['GET'])
@jwt_required
def get_all_projets():
    current_app.logger.info('In GET /projets')
    session = Session()
    projets_objects = session.query(Projet).all()

    # Transforming into JSON-serializable objects
    schema = ProjetSchema(many=True)
    projets = schema.dump(projets_objects)

    # Serializing as JSON
    session.close()
    return jsonify(projets)


@resources.route('/projets/<int:proj_id>', methods=['GET'])
@jwt_required
def get_projet_by_id(proj_id):
    current_app.logger.info('In GET /projets/<int>')
    check_projet_exists(proj_id)

    session = Session()
    projet_object = session.query(Projet).filter_by(id_p=proj_id).all()

    # Transforming into JSON-serializable objects
    schema = ProjetSchema(many=True)
    projet = schema.dump(projet_object)

    # Serializing as JSON
    session.close()
    return jsonify(projet)


@resources.route('/projets/<int:proj_id>', methods=['PUT'])
@jwt_required
def update_user(proj_id):
    current_app.logger.info('In PUT /projets/<int>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = proj_id

    # Check if project exists
    check_projet_exists(proj_id)

    data = ProjetSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u')) \
        .load(data)
    projet = Projet(**data)

    session = Session()
    session.merge(projet)
    session.commit()

    updated_projet = ProjetSchema().dump(projet)
    session.close()
    return jsonify(updated_projet), 200


@resources.route('/projets/<int:proj_id>', methods=['DELETE'])
@jwt_required
def delete_projet(proj_id):
    check_projet_exists(proj_id)

    session = Session()
    projet = session.query(Projet).filter_by(id_f=proj_id).first()
    session.delete(projet)
    session.commit()
    session.close()
    return jsonify({
        'message': f'Le projet avec l\'identifiant {proj_id} a été supprimé'
    }), 204


def check_projet_exists(proj_id):
    try:
        session = Session()
        existing_proj = session.query(Projet).filter_by(id_p=proj_id).first()
        session.close()
        if existing_proj is None:
            raise ValueError('This projet does not exist')
    except ValueError:
        resp = jsonify({"error": {
            'code': 'PROJET_NOT_FOUND',
            'message': f'Projet with id {proj_id} does not exist.'
        }})
        resp.status_code = 404
        return resp
