from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required

from .db_services import FundingDBService
from .validation_service import FundingValidationService
from src.api.projects.db_service import ProjectDBService
from src.api.funders.db_services import FunderDBService
import sqlalchemy

resources = Blueprint('fundings', __name__)


@resources.route('/api/projects/<int:project_id>/fundings', methods=['GET'])
@jwt_required
def get_fundings_by_project(project_id: int):
    """This function get all fundings referenced by the project passed in the parameter

    Args:
        project_id (int): id of project

    Returns:
        Response: list of fundings
    """
    current_app.logger.debug('In GET /api/projects/<int:project_id>/fundings')
    response = None
    try:
        # Checks if project exist
        ProjectDBService.get_project_by_id(project_id)  
        response = FundingDBService.get_fundings_by_project(project_id)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des données financements'}), 500
    finally:
        return response


@resources.route('/api/funders/<int:funder_id>/fundings', methods=['GET'])
@jwt_required
def get_fundings_by_funder(funder_id: int):
    """This function get all fundings referenced by his funder

    Args:
        funder_id (int): id of funder

    Returns:
        Response: list of fundings
    """
    current_app.logger.debug('In GET /api/funders/<int:funder_id>/fundings')
    response = None
    try:
        # Checks if funder exist
        FunderDBService.get_funder_by_id(funder_id)
        response = FundingDBService.get_funding_by_funder(funder_id)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des données financements'}), 500
    finally:
        return response


@resources.route('/api/fundings', methods=['POST'])
@jwt_required
def add_funding():
    """This function created a new funding

    Returns:
        Response: funding created
    """
    current_app.logger.debug('In POST /api/fundings')
    response = None
    try:
        # Load data
        posted_funding = request.get_json()
        # Check posted data fields
        FundingValidationService.validate(posted_funding)
        # Checks project exist
        ProjectDBService.get_project_by_id(posted_funding['id_p'])
        # Insert
        response = FundingDBService.insert(posted_funding)
        response = jsonify(response), 201
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement du financement'}), 500
    finally:
        return response


@resources.route('/api/fundings/<int:funding_id>', methods=['PUT'])
@jwt_required
def update_funding(funding_id: int):
    """This function update a funding

    Args:
        funding_id (int): id of funding

    Returns:
        Response: description of funding updated
    """
    current_app.logger.debug('In PUT /api/fundings/<int:funding_id>')
    response = None
    try:
        # Load data
        data = request.get_json()
        if 'id_f' not in data:
            data['id_f'] = funding_id
        
        # Check can modify
        FundingDBService.can_update(data['id_p'])
        # Validate fields to update
        FundingValidationService.validate(data)
        # Checks
        FundingDBService.get_funding_by_id(data['id_f'])
        
        response = FundingDBService.update(data)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la modification du financement'}), 500
    finally:
        return response


@resources.route('/api/fundings/<int:funding_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_funding(funding_id: int):
    """This function delete a funding refernced by his id

    Args:
        funding_id (int): id of funding

    Returns:
    """
    current_app.logger.debug('In DELETE /api/fundings/<int:funding_id>')
    try:
        # Check if project exists
        FundingDBService.get_funding_by_id(funding_id)
        # Delete others entity referenced if exist
        FundingDBService.delete_entities_referenced(funding_id)

        response = FundingDBService.delete(funding_id)
        response = jsonify(response), 204
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression du financement'}), 500
    finally:
        return response
