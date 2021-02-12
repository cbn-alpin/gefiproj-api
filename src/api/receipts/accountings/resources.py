from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from src.api.users.auth_resources import admin_required
from .db_services import ReceiptAccountingDBService
from .validation_service import ReceiptAccountingValidationService

resources = Blueprint('receipts_accountings', __name__)


@resources.route('/api/receipts/accountings', methods=['GET'])
@jwt_required
def get_receipts_accountings():
    current_app.logger.debug('In GET /api/receipts/accountings')
    response = None
    try:
        # Checks
        response = ReceiptAccountingDBService.get_receipts_accountings()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des recettes comptables'}), 500
    finally:
        return response


@resources.route('/api/receipts/accountings', methods=['POST'])
@jwt_required
@admin_required
def add_receipt_accounting():
    current_app.logger.debug('In POST /api/receipts/accountings')
    response = None
    try:
        # Load data
        data = request.get_json()
        # check posted data fields
        ReceiptAccountingValidationService.validate_post(data)
        # check year
        ReceiptAccountingDBService.check_unique_year(data['annee_rc'])

        response = ReceiptAccountingDBService.insert(data)
        response = jsonify(response), 201
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement de la recette comptable'}), 500
    finally:
        return response


@resources.route('/api/receipts/accountings/<int:receipt_accounting_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_receipt_accounting(receipt_accounting_id):
    current_app.logger.debug('In PUT /api/receipts/accountings/<int:receipt_accounting_id>')
    response = None
    try:
        # Load data
        data = request.get_json()
        if 'id_rc' not in data:
            data['id_rc'] = receipt_accounting_id

        # validate fields to update
        ReceiptAccountingValidationService.validate_post(data)
        # check
        ReceiptAccountingDBService.get_receipt_accounting_by_id(receipt_accounting_id)
        # Checks if year is unique
        ReceiptAccountingDBService.check_unique_year(data['annee_rc'], receipt_accounting_id)

        response = ReceiptAccountingDBService.update(data)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la modification de la recette comptable'}), 500
    finally:
        return response


@resources.route('/api/receipts/accountings/<int:receipt_accounting_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_expense(receipt_accounting_id: int):
    current_app.logger.debug('In DELETE /api/receipts/accountings/<int:receipt_accounting_id>')
    response = None
    try:
        # check
        receipt = ReceiptAccountingDBService.get_receipt_accounting_by_id(receipt_accounting_id)

        response = ReceiptAccountingDBService.delete(receipt_accounting_id)
        response = jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression de la recette comptable'}), 500
    finally:
        return response
