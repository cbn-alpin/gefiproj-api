from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required
from .db_services import FunderDBService
from .validation_service import FunderValidationService

resources = Blueprint('funders', __name__)


@resources.route('/api/funders', methods=['GET'])
@jwt_required
def get_funders():
    try:
        current_app.logger.debug('In GET /api/funders')

        response = FunderDBService.get_all_funders()
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@resources.route('/api/funders', methods=['POST'])
@jwt_required
def add_funder():
    try:
        current_app.logger.debug('In POST /api/funders')
        # Load data
        posted_funder_data = request.get_json()
        # check posted data fields
        validation_errors = FunderValidationService.validate_post(posted_funder_data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
        # check
        FunderDBService.check_unique_funder_name(posted_funder_data['nom_financeur'])

        response = FunderDBService.insert(posted_funder_data)
        return jsonify(response), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/funders/<int:funder_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_funder(funder_id):
    try:
        current_app.logger.debug('In PUT /api/funders/<int:funder_id>')
        # Load data
        data = request.get_json()
        if 'id_financeur' not in data:
            data['id_financeur'] = funder_id
            
        # validate fields to update
        validation_errors = FunderValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
        # check
        FunderDBService.check_exist_funder(funder_id)
        FunderDBService.check_unique_funder_name(data['nom_financeur'])
        
        response = FunderDBService.update(data)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/funders/<int:funder_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_funder(funder_id):
    try:
        current_app.logger.debug('In DELETE /api/funders/<int:funder_id>')
        # check
        FunderDBService.check_exist_funder(funder_id)
        FunderDBService.check_funder_use_in_funding(funder_id)

        response = FunderDBService.delete(funder_id)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
