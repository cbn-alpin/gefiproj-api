from flask import Blueprint, current_app, jsonify, request, Response
from .db_services import FundingDBService
from .validation_service import FundingValidationService
resources = Blueprint('funding', __name__)


@resources.route('/api/projects/<int:project_id>/fundings', methods=['GET'])
#@jwt_required
def get_fundings_by_project(project_id):
    try:
        current_app.logger.debug('In GET /api/projects/<int:project_id>/fundings')
        # Checks
        FundingDBService.check_project_exists(project_id)  
        response = FundingDBService.get_funding_by_project(project_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/funding', methods=['POST'])
#@jwt_required
# @admin_required('admin')
def add_funding():
    try:
        current_app.logger.debug('In POST /api/funding')
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


@resources.route('/api/funding/<int:funding_id>', methods=['PUT'])
#@jwt_required
# @admin_required('admin')
def update_funding(funding_id):
    try:
        current_app.logger.debug('In PUT /api/funding/<int:funding_id>')
        # Load data
        data = request.get_json()
        if 'id_f' not in data:
            data['id_f'] = funding_id
            
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


@resources.route('/api/funding/<int:funding_id>', methods=['DELETE'])
# @jwt_required
# @admin_required('admin')
def delete_funding(funding_id):
    try:
        # check
        FundingDBService.check_funding_exists(funding_id)

        response = FundingDBService.delete_funding(funding_id)
        print(response)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
