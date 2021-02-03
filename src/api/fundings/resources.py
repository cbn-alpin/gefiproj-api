from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required
from .db_services import FundingDBService
from .validation_service import FundingValidationService

resources = Blueprint('fundings', __name__)


@resources.route('/api/projects/<int:project_id>/fundings', methods=['GET'])
@jwt_required
def get_fundings_by_project(project_id):
    try:
        current_app.logger.debug('In GET /api/projects/<int:project_id>/fundings')
        # Checks
        FundingDBService.check_project_exists(project_id)  
        response = FundingDBService.get_funding_by_project(project_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@resources.route('/api/funders/<int:funder_id>/fundings', methods=['GET'])
@jwt_required
def get_fundings_by_funder(funder_id):
    try:
        current_app.logger.debug('In GET /api/funders/<int:funder_id>/fundings')

        response = FundingDBService.get_funding_by_funder(funder_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@resources.route('/api/fundings', methods=['POST'])
@jwt_required
def add_funding():
    try:
        current_app.logger.debug('In POST /api/fundings')
        # Load data
        posted_funding = request.get_json()
        # check posted data fields
        validation_errors = FundingValidationService.validate_post(posted_funding)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422

        # Checks
        FundingDBService.check_project_exists(posted_funding['id_p'])
        
        response = FundingDBService.insert_funding(posted_funding)
        return jsonify(response), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/fundings/<int:funding_id>', methods=['PUT'])
@jwt_required
def update_funding(funding_id):
    try:
        current_app.logger.debug('In PUT /api/fundings/<int:funding_id>')
        # Load data
        data = request.get_json()
        if 'id_f' not in data:
            data['id_f'] = funding_id
        
        # check can modify
        FundingDBService.can_update(data['id_p'])
        # validate fields to update
        validation_errors = FundingValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
            
        # Checks
        FundingDBService.check_funding_exists(data['id_f'])
        
        response = FundingDBService.update_funding(data)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/fundings/<int:funding_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_funding(funding_id):
    try:
        current_app.logger.debug('In DELETE /api/fundings/<int:funding_id>')
        # check
        FundingDBService.check_funding_exists(funding_id)
        FundingDBService.delete_children(funding_id)

        response = FundingDBService.delete_funding(funding_id)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
