from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

from .db_services import ReceiptAccountingDBService
from .validation_service import ReceiptAccountingValidationService
from ..users.auth_resources import admin_required

resources = Blueprint('receipts_accountings', __name__)


@resources.route('/api/receipts/accountings', methods=['GET'])
@jwt_required
def get_receipts_accountings():
    try:
        current_app.logger.debug('In GET /api/receipts/accountings')
        # Checks
        response = ReceiptAccountingDBService.get_receipts_accountings()
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/accountings', methods=['POST'])
@jwt_required
def add_receipt_accounting():
    try:
        current_app.logger.debug('In POST /api/receipts/accountings')
        # Load data
        data = request.get_json()
        
        # check posted data fields
        validation_errors = ReceiptAccountingValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occurred',
                'errors': validation_errors
            }), 422

        # check 
        ReceiptAccountingDBService.check_unique_year(data['annee_rc'])

        response = ReceiptAccountingDBService.insert(data)
        return jsonify(response), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/accountings/<int:receipt_accounting_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_receipt_accounting(receipt_accounting_id):
    try:
        current_app.logger.debug('In PUT /api/receipts/accountings/<int:receipt_accounting_id>')
        # Load data
        data = request.get_json()
        if 'id_rc' not in data:
            data['id_rc'] = receipt_accounting_id
            
        # validate fields to update
        validation_errors = ReceiptAccountingValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occurred',
                'errors': validation_errors
            }), 422
        # check
        ReceiptAccountingDBService.check_exist_receipt_accounting(receipt_accounting_id)
        ReceiptAccountingDBService.check_unique_year(data['annee_rc'], receipt_accounting_id)
        
        response = ReceiptAccountingDBService.update(data)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]
    
    
@resources.route('/api/receipts/accountings/<int:receipt_accounting_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_expense(receipt_accounting_id):
    try:
        current_app.logger.debug('In DELETE /api/receipts/accountings/<int:receipt_accounting_id>')
        # check
        ReceiptAccountingDBService.check_exist_receipt_accounting(receipt_accounting_id)

        response = ReceiptAccountingDBService.delete(receipt_accounting_id)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
