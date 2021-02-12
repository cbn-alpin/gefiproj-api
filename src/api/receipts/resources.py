from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from .db_services import ReceiptDBService
from .validation_service import ReceiptValidationService
from ..fundings.db_services import FundingDBService
from ..users.auth_resources import admin_required

resources = Blueprint('receipts', __name__)


@resources.route('/api/fundings/<int:funding_id>/receipts', methods=['GET'])
@jwt_required
def get_receipts_by_funding(funding_id: int):
    current_app.logger.debug('In GET /api/fundings/<int:funding_id>/receipts')
    response = None
    try:
        # Checks
        FundingDBService.get_funding_by_id(funding_id)
        response = ReceiptDBService.get_receipts_by_funding_id(funding_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as error:
        current_app.logger.error(error)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des recettes'}), 500
    finally:
        return response


@resources.route('/api/receipts', methods=['POST'])
@jwt_required
@admin_required
def add_receipt():
    current_app.logger.debug('In POST /api/receipts')
    response = None
    try:
        posted_receipt_data = request.get_json()

        # Check posted data fields
        ReceiptValidationService.validate_post(posted_receipt_data)
        # Check funding
        FundingDBService.get_funding_by_id(posted_receipt_data['id_f'])
        # Check project not solde
        ReceiptDBService.is_project_solde(funding_id = posted_receipt_data['id_f'])
        # Check there is no receipt for this funding this year
        ReceiptDBService.get_receipts_of_year_by_funding_id(posted_receipt_data['id_f'], posted_receipt_data['annee_r'])
        # Check sum amount value
        ReceiptDBService.check_sum_value(posted_receipt_data)
        
        created_receipt = ReceiptDBService.insert(posted_receipt_data)
        response = jsonify(created_receipt), 201
    except ValueError as error:
        response = jsonify(error.args[0]), error.args[1]
    except Exception as error:
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement de la recette'}), 500
    finally:
        return response


@resources.route('/api/receipts/<int:id_receipt>', methods=['PUT'])
@jwt_required
@admin_required
def update_receipt(id_receipt: int):
    current_app.logger.debug('In PUT /api/receipts/<int:id_receipt>')
    response = None
    try:
        data = request.get_json()
        data['id_r'] = id_receipt
        
        # Validate fields to update
        ReceiptValidationService.validate_post(data)
        # Check if receipt exists
        receipt = ReceiptDBService.get_receipt_by_id(id_receipt)
        # Check project not solde
        ReceiptDBService.is_project_solde(funding_id = data['id_f'])
        # Check there is no receipt for this funding this year
        ReceiptDBService.get_receipts_of_year_by_funding_id(data['id_f'], data['annee_r'], id_receipt)
        # Check sum amount value
        ReceiptDBService.check_sum_value(data, id_receipt)
        
        updated_receipt = ReceiptDBService.update(data)
        response = jsonify(updated_receipt), 200
    except ValueError as error:
        response = jsonify(error.args[0]), error.args[1]
    except Exception as error:
        response = jsonify({'message': 'Une erreur est survenue lors de la modification de la recette'}), 500
    finally:
        return response


@resources.route('/api/receipts/<int:id_receipt>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_receipt(id_receipt: int):
    current_app.logger.debug('In DELETE /api/receipts/<int:id_receipt>')
    response = None
    try:
        # check if receipt exists
        receipt = ReceiptDBService.get_receipt_by_id(id_receipt)
        # check if project status is 'SOLDE'
        ReceiptDBService.is_project_solde(id_receipt = id_receipt)

        # delete the receipt
        response = ReceiptDBService.delete(id_receipt, receipt['annee_r'])
        response = jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression de la recette'}), 500
    finally:
        return response
