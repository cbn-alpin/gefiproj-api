from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from ..users.auth_resources import admin_required

from .db_services import AmountDBService
from .validation_service import AmountValidationService
from src.api.receipts.db_services import ReceiptDBService

resources = Blueprint('amounts', __name__)


@resources.route('/api/receipts/<int:receipt_id>/amounts', methods=['GET'])
@jwt_required
def get_amounts_by_receipt(receipt_id: int):
    """This function get all amount by it receipt referenced

    Args:
        receipt_id (int): id of receipt

    Returns:
        Response: list of amounts
    """
    current_app.logger.debug('In GET /api/receipts/<int:receipt_id>/amounts')
    response = None
    try:
        # Checks if receipt is exist
        ReceiptDBService.get_receipt_by_id(receipt_id)  
        response = AmountDBService.get_amount_by_receipt_id(receipt_id)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/amounts', methods=['POST'])
@jwt_required
def add_amount():
    """This function created a new amount

    Returns:
        Response: amount created
    """
    current_app.logger.debug('In POST /api/amounts')
    response = None
    try:
        # Load data
        posted_amount = request.get_json()
        # Check posted data fields
        AmountValidationService.validate(posted_amount)
        # Check receipt
        ReceiptDBService.get_receipt_by_id(posted_amount['id_r'])
        AmountDBService.check_unique_amount_by_year_and_receipt_id(posted_amount['annee_ma'], posted_amount['id_r'])
        AmountDBService.check_sum_value(posted_amount)
        
        response = AmountDBService.insert(posted_amount)
        response = jsonify(response), 201
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/amounts/<int:amount_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_amount(amount_id: int):
    """This function update a data of amount
    
    Args:
        amount_id (int): id of amount

    Returns:
        Response: description of amount
    """
    current_app.logger.debug('In PUT /api/amounts/<int:amount_id>')
    response = None
    try:
        # Load data
        data = request.get_json()
        if 'id_ma' not in data:
            data['id_ma'] = amount_id
            
        # Validate fields to update
        AmountValidationService.validate(data)
        # Checks
        ReceiptDBService.get_receipt_by_id(data['id_r'])
        AmountDBService.check_unique_amount_by_year_and_receipt_id(data['annee_ma'], data['id_r'], amount_id)
        AmountDBService.check_sum_value(data, amount_id)
        
        response = AmountDBService.update(data)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/amounts/<int:amount_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_amount(amount_id: int):
    """This function delete a amount
    
    Args:
        amount_id (int): id of amount

    Returns:
    """
    current_app.logger.debug('In DELETE /api/amounts/<int:amount_id>')
    response = None
    try:
        # Check
        ReceiptDBService.get_receipt_by_id(amount_id)

        response = AmountDBService.delete(amount_id)
        response = jsonify(response), 204
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response
