from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required

from .db_services import FunderDBService
from .validation_service import FunderValidationService

resources = Blueprint('funders', __name__)


@resources.route('/api/funders', methods=['GET'])
@jwt_required
def get_all_funders():
    """This function get all funders

    Returns:
        Response: list of funders
    """
    current_app.logger.debug('In GET /api/funders')
    response = None
    try:
        response = FunderDBService.get_all_funders()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des financeurs'}), 500
    finally:
        return response


@resources.route('/api/funders', methods=['POST'])
@jwt_required
@admin_required
def add_funder():
    """This function created a new funder

    Returns:
        Response: funder created
    """
    current_app.logger.debug('In POST /api/funders')
    response = None
    try:
        # Load data
        posted_funder = request.get_json()
        # Check posted data fields
        FunderValidationService.validate(posted_funder)
        # Checks if name funder is unique
        FunderDBService.check_unique_funder_name(posted_funder['nom_financeur'])
        # Insert
        response = FunderDBService.insert(posted_funder)
        response = jsonify(response), 201
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement du financement'}), 500
    finally:
        return response


@resources.route('/api/funders/<int:funder_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_funder(funder_id: int):
    """This function update a data of funder

    Args:
        funder_id (int): id of funder

    Returns:
        Response: description of funder
    """
    current_app.logger.debug('In PUT /api/funders/<int:funder_id>')
    response = None
    try:
        # Load data
        data = request.get_json()
        if 'id_financeur' not in data:
            data['id_financeur'] = funder_id
        # Check data fields
        FunderValidationService.validate(data)
        # Checks if funder exist
        FunderDBService.get_funder_by_id(funder_id)
        # Checks if name funder is unique
        FunderDBService.check_unique_funder_name(data['nom_financeur'], funder_id)
        
        response = FunderDBService.update(data)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la modification du financeur'}), 500
    finally:
        return response



@resources.route('/api/funders/<int:funder_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_funder(funder_id: int):
    """This function delete a funder

    Args:
        funder_id (int): id of funder

    Returns:
        Response: description of funder
    """
    current_app.logger.debug('In DELETE /api/funders/<int:funder_id>')
    response = None
    try:
        # Check if funder exists
        funder = FunderDBService.get_funder_by_id(funder_id)
        # Check if funder is referenced to fundings
        FunderDBService.check_funder_referenced_in_funding(funder_id, funder['nom_financeur'])

        response = FunderDBService.delete(funder_id, funder['nom_financeur'])
        response = jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression du financement'}), 500
    finally:
        return response
