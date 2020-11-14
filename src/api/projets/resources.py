from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from shared.entity import Session

from .db_service import ProjectDBService
from .entities import Projet, ProjetSchema
from .validation_service import ProjetValidationService
from ..financements.db_services import FinancementDBService
from ..users.db_services import check_user_exists_by_id

resources = Blueprint('projets', __name__)


@resources.route('/api/projets', methods=['POST'])
@jwt_required
def add_projet():
    current_app.logger.debug('In POST /api/projets')
    posted_data = request.get_json()

    # check posted data fields
    validation_errors = ProjetValidationService.validate_post(posted_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    # convert posted data into project
    posted_projet = ProjetSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u')) \
        .load(posted_data)
    projet = Projet(**posted_projet)

    # check if user with id_u exists
    user_error = check_user_exists_by_id(projet.id_u)
    if user_error is not None:
        return jsonify(user_error), 404

    # check if project code doesn't already exist
    project_by_code = ProjectDBService.check_projet_exists_by_code(projet.code_p)
    if project_by_code is None:
        return jsonify({
            'code': 'CODE_PROJET_ALREADY_EXISTS',
            'message': f'A project with code <{projet.code_p}> already exists'
        }), 422

    # check if project name doesn't already exist
    project_by_name = ProjectDBService.check_projet_exists_by_name(projet.nom_p)
    if project_by_name is None:
        return jsonify({
            'code': 'NAME_PROJET_ALREADY_EXISTS',
            'message': f'A project with name <{projet.nom_p}> already exists'
        })

    # add the projet to db and return it
    session = Session()
    session.add(projet)
    session.commit()

    new_projet = ProjetSchema().dump(projet)
    return jsonify(new_projet), 201


@resources.route('/api/projets', methods=['GET'])
@jwt_required
def get_all_projets():
    current_app.logger.info('In GET /api/projets')

    query_params = request.args
    query_error = ProjetValidationService.validate_get_all(query_params)
    if len(query_error) > 0:
        return jsonify(query_error), 422

    limit = query_params.get('limit', default=10)
    offset = query_params.get('offset', default=0)
    return jsonify(ProjectDBService.get_all_projets(limit, offset))


@resources.route('/api/projets/<int:proj_id>', methods=['GET'])
@jwt_required
def get_projet_by_id(proj_id):
    current_app.logger.info('In GET /api/projets/<int>')

    # check if the project exists
    exist_error = ProjectDBService.check_projet_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    return jsonify(ProjectDBService.get_projet_by_id(proj_id))


@resources.route('/api/projets/<int:proj_id>', methods=['PUT'])
@jwt_required
def update_projet(proj_id):
    current_app.logger.info('In PUT /api/projets/<int>')

    posted_data = request.get_json()
    if 'id_p' not in posted_data:
        posted_data['id_p'] = proj_id

    # validate fields to update
    validation_errors = ProjetValidationService.validate_post(posted_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    posted_data = ProjetSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u', 'id_p')) \
        .load(posted_data)
    project_to_update = Projet(**posted_data)

    # check if the project exists
    exist_error = ProjectDBService.check_projet_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    # check if user with id_u exists
    user_error = check_user_exists_by_id(project_to_update.id_u)
    if user_error is not None:
        return jsonify(user_error), 404

    # check project code and name are not used
    project_by_code = ProjectDBService.get_projet_by_code(project_to_update.code_p)
    if 'id_p' in project_by_code and project_by_code.get('id_p') != proj_id:
        return jsonify({
            'code': 'CODE_PROJET_ALREADY_EXISTS',
            'message': f'A project with code <{project_to_update.code_p}> already exists'
        }), 422

    project_by_name = ProjectDBService.get_projet_by_nom(project_to_update.nom_p)
    if 'id_p' in project_by_name and project_by_name.get('id_p') != proj_id:
        return jsonify({
            'code': 'NAME_PROJET_ALREADY_EXISTS',
            'message': f'A project with name <{project_to_update.nom_p}> already exists'
        }), 422

    return jsonify(ProjectDBService.update_projet(project_to_update)), 200


@resources.route('/api/projets/<int:proj_id>', methods=['DELETE'])
@jwt_required
def delete_projet(proj_id):
    current_app.logger.info('In DELETE /api/projets/<int>')

    exist_error = ProjectDBService.check_projet_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    # can delete not linked to any financement
    linked_fin = FinancementDBService.get_financements_by_projet_id(proj_id)
    if 'id_f' in linked_fin:
        return jsonify({
            'code': 'PROJECT_HAS_FNANCEMENT',
            'message': f'Cannot delete project <{proj_id}> because it is linked to financement <{linked_fin.id_f}>'
        })

    # ??? droit de supprimer si projet non soldé

    id_deleted = ProjectDBService.delete_projet(proj_id)
    return jsonify({
        'message': f'Le projet avec l\'identifiant {id_deleted} a été supprimé'
    }), 204
