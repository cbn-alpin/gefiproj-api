from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from .db_service import ProjectDBService
from .entities import Project, ProjectSchema
from .validation_service import ProjectValidationService
from ..fundings.db_services import FundingDBService
from ..users.db_services import UserDBService

resources = Blueprint('projects', __name__)


@resources.route('/api/projects', methods=['POST'])
@jwt_required
def add_project():
    current_app.logger.debug('In POST /api/projects')
    posted_data = request.get_json()

    # check posted data fields
    validation_errors = ProjectValidationService.validate_post(posted_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    # convert posted data into project
    posted_project = ProjectSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u')) \
        .load(posted_data)
    project = Project(**posted_project)

    # check if user with id_u exists
    user_error = UserDBService.check_user_exists_by_id(project.id_u)
    if user_error is not None:
        return jsonify(user_error), 404

    # check if project code doesn't already exist
    project_by_code = ProjectDBService.check_project_exists_by_code(project.code_p)
    if project_by_code is None:
        return jsonify({
            'code': 'CODE_PROJECT_ALREADY_EXISTS',
            'message': f'A project with code <{project.code_p}> already exists'
        }), 422

    # check if project name doesn't already exist
    project_by_name = ProjectDBService.check_project_exists_by_name(project.nom_p)
    if project_by_name is None:
        return jsonify({
            'code': 'NAME_PROJECT_ALREADY_EXISTS',
            'message': f'A project with name <{project.nom_p}> already exists'
        })

    # add the project to db and return it
    project = ProjectDBService.insert_project(project)

    new_project = ProjectSchema().dump(project)
    return jsonify(new_project), 201


@resources.route('/api/projects', methods=['GET'])
@jwt_required
def get_all_projects():
    current_app.logger.info('In GET /api/projects')

    query_params = request.args
    query_error = ProjectValidationService.validate_get_all(query_params)
    if len(query_error) > 0:
        return jsonify(query_error), 422

    limit = query_params.get('limit', default=10)
    offset = query_params.get('offset', default=0)
    return jsonify(ProjectDBService.get_all_projects(limit, offset))


@resources.route('/api/projects/<int:proj_id>', methods=['GET'])
@jwt_required
def get_project_by_id(proj_id):
    current_app.logger.info('In GET /api/projects/<int>')

    # check if the project exists
    exist_error = ProjectDBService.check_project_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    return jsonify(ProjectDBService.get_project_by_id(proj_id))


@resources.route('/api/projects/<int:proj_id>', methods=['PUT'])
@jwt_required
def update_project(proj_id):
    current_app.logger.info('In PUT /api/projects/<int>')

    posted_data = request.get_json()
    if 'id_p' not in posted_data:
        posted_data['id_p'] = proj_id

    # validate fields to update
    validation_errors = ProjectValidationService.validate_post(posted_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    posted_data = ProjectSchema(only=('code_p', 'nom_p', 'statut_p', 'id_u', 'id_p')) \
        .load(posted_data)
    project_to_update = Project(**posted_data)

    # check if the project exists
    exist_error = ProjectDBService.check_project_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    # check if user with id_u exists
    user_error = UserDBService.check_user_exists_by_id(project_to_update.id_u)
    if user_error is not None:
        return jsonify(user_error), 404

    # check project code and name are not used
    project_by_code = ProjectDBService.get_project_by_code(project_to_update.code_p)
    if 'id_p' in project_by_code and project_by_code.get('id_p') != proj_id:
        return jsonify({
            'code': 'CODE_PROJECT_ALREADY_EXISTS',
            'message': f'A project with code <{project_to_update.code_p}> already exists'
        }), 422

    project_by_name = ProjectDBService.get_project_by_nom(project_to_update.nom_p)
    if 'id_p' in project_by_name and project_by_name.get('id_p') != proj_id:
        return jsonify({
            'code': 'NAME_PROJECT_ALREADY_EXISTS',
            'message': f'A project with name <{project_to_update.nom_p}> already exists'
        }), 422

    return jsonify(ProjectDBService.update_project(project_to_update)), 200


@resources.route('/api/projects/<int:proj_id>', methods=['DELETE'])
@jwt_required
def delete_project(proj_id):
    current_app.logger.info('In DELETE /api/projects/<int>')

    exist_error = ProjectDBService.check_project_exists_by_id(proj_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    # can delete not linked to any funding
    linked_fin = FundingDBService.get_funding_by_project_id(proj_id)
    if 'id_f' in linked_fin:
        return jsonify({
            'code': 'PROJECT_HAS_FNANCEMENT',
            'message': f'Cannot delete project <{proj_id}> because it is linked to funding <{linked_fin.id_f}>'
        }), 403

    # ??? droit de supprimer si projet non soldé

    id_deleted = ProjectDBService.delete_project(proj_id)
    return jsonify({
        'message': f'Le projet avec l\'identifiant {id_deleted} a été supprimé'
    }), 204
