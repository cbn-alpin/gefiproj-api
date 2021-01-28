from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from .db_services import AmountDBService
from .validation_service import AmountValidationService
from ..users.auth_resources import admin_required

resources = Blueprint('amounts', __name__)


@resources.route('/api/receipts/<int:receipt_id>/amounts', methods=['GET'])
@jwt_required
def get_amounts_by_receipt(receipt_id):
    try:
        current_app.logger.debug('In GET /api/receipts/<int:receipt_id>/amounts')
        # Checks
        AmountDBService.check_receipt_exists_by_id(receipt_id)  
        response = AmountDBService.get_amount_by_receipt_id(receipt_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/amounts', methods=['POST'])
@jwt_required
def add_amount():
    try:
        current_app.logger.debug('In POST /api/amounts')
        # Load data
        posted_amount_data = request.get_json()
        # check posted data fields
        validation_errors = AmountValidationService.validate_post(posted_amount_data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422

        # check receipt
        AmountDBService.check_receipt_exists_by_id(posted_amount_data['id_r'])
        
        response = AmountDBService.insert(posted_amount_data)
        return jsonify(response), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/amounts/<int:amount_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_amount(amount_id):
    try:
        current_app.logger.debug('In PUT /api/amounts/<int:amount_id>')
        # Load data
        data = request.get_json()
        if 'id_ma' not in data:
            data['id_ma'] = amount_id
            
        # validate fields to update
        validation_errors = AmountValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
            
        # Checks
        AmountDBService.check_receipt_exists_by_id(data['id_r'])
        
        response = AmountDBService.update(data)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/amounts/<int:amount_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_amount(amount_id):
    try:
        current_app.logger.debug('In DELETE /api/amounts/<int:amount_id>')
        # check
        AmountDBService.check_amount_exists_by_id(amount_id)

        response = AmountDBService.delete(amount_id)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
