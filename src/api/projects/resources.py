from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from ..users.auth_resources import admin_required

from .db_service import ProjectDBService
from .validation_service import ProjectValidationService
from ..fundings.db_services import FundingDBService, Status
from ..users.db_services import UserDBService

resources = Blueprint('projects', __name__)


@resources.route('/api/projects', methods=['POST'])
@jwt_required
@admin_required
def add_project():
    """This function add a new project

    Returns:
        Response: the project created
    """
    current_app.logger.debug('In POST /api/projects')
    response = None
    try:
        posted_data = request.get_json()
        # Validate user posted data
        ProjectValidationService.validate_form(posted_data)
        # Check if project code and name doesn't already exist
        ProjectDBService.check_unique_code_and_name(posted_data['code_p'], posted_data['nom_p'])
        # Check if user with id_u exists
        UserDBService.get_user_by_id(posted_data['id_u'])

        response = ProjectDBService.insert(posted_data)
        response = jsonify(response), 201
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement du projet'}), 500
    finally:
        return response


@resources.route('/api/projects', methods=['GET'])
@jwt_required
def get_all_projects():
    """This function get all projects

    Returns:
        Response: list of projects
    """
    current_app.logger.info('In GET /api/projects')
    response = None
    try:
        query_params = request.args
        query_error = ProjectValidationService.validate_get_all(query_params)
        response = ProjectDBService.get_all_projects()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des données projets'}), 500
    finally:
        return response


@resources.route('/api/projects/<int:project_id>', methods=['GET'])
@jwt_required
def get_project_by_id(project_id: int):
    """This function get one project by his id referenced

    Args:
        project_id (int): id of project

    Returns:
        Response: description of one project
    """
    current_app.logger.info('In GET /api/projects/<int:project_id>')
    response = None
    try:
        project = ProjectDBService.get_project_by_id(project_id)
        response = jsonify(project), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des données projets'}), 500
    finally:
        return response


@resources.route('/api/projects/<int:project_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_project(project_id: int):
    """This function upate a data of project

    Args:
        project_id (int): id of project

    Returns:
        Response: description of project
    """
    current_app.logger.info('In PUT /api/projects/<int:project_id>')
    response = None
    try:
        posted_data = request.get_json()
        if 'id_p' not in posted_data:
            posted_data['id_p'] = project_id
            
        # Check forms
        ProjectValidationService.validate_form(posted_data)
        # Check if project exists
        ProjectDBService.get_project_by_id(project_id)
        # Check if code_p or nom_p are already in use
        ProjectDBService.check_unique_code_and_name(posted_data['code_p'], posted_data['nom_p'], project_id)
        # Check if user with id_u exists
        UserDBService.get_user_by_id(posted_data['id_u'])
        # Check if project solde don't have funding not solde
        if posted_data['statut_p'] == True:
            FundingDBService.check_fundings_not_solde_by_project(project_id)
            
        response = ProjectDBService.update(posted_data)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la modification des données du projet'}), 500
    finally:
        return response


@resources.route('/api/projects/<int:project_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_project(project_id: int):
    """This function delete a project referenced by his id

    Args:
        project_id (int): id of project

    Returns:
        Response: 
    """
    current_app.logger.info('In DELETE /api/projects/<int:project_id>')
    try:
        # Check if project exists
        project = ProjectDBService.get_project_by_id(project_id)
        # Check if project has fundings referenced
        FundingDBService.check_project_not_have_funding(project_id)
        
        response = ProjectDBService.delete(project_id, project['nom_p'])
        response = jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression du projet'}), 500
    finally:
        return response
