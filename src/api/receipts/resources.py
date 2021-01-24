from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

from .db_services import ReceiptDBService
from .entities import ReceiptSchema, Receipt
from .validation_service import ReceiptValidationService
from ..fundings.db_services import FundingDBService
from ..users.auth_resources import admin_required

resources = Blueprint('receipts', __name__)


@resources.route('/api/fundings/<int:funding_id>/receipts', methods=['GET'])
def get_receipts_by_funding(funding_id):
    try:
        current_app.logger.debug('In GET /api/fundings/<int:funding_id>/receipts')
        # Checks
        ReceiptDBService.check_funding_exists(funding_id)
        response = ReceiptDBService.get_receipts_by_funding_id(funding_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts', methods=['POST'])
@jwt_required
@admin_required
def add_receipt():
    current_app.logger.debug('In POST /api/receipts')
    posted_receipt_data = request.get_json()

    validation_errors = ReceiptValidationService.validate_post(posted_receipt_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    posted_receipt = ReceiptSchema(only=('id_f', 'montant_r', 'annee_r')).load(posted_receipt_data, unknown=EXCLUDE)
    receipt = Receipt(**posted_receipt)

    # check funding
    FundingDBService.check_funding_exists(receipt.id_f)

    # check there is no receipt for this funding this yeat
    receipts_of_year = ReceiptDBService.get_receipts_of_year_by_funding_id(receipt.id_f, receipt.annee_r)
    if len(receipts_of_year) > 0:
        return jsonify({
            'status': 'error',
            'type': 'CONFLICT',
            'code': 'FUNDING_HAS_RECEIPT',
            'message': f"The funding {receipt.id_f} already has a receipt for the year {receipt.annee_r}."
        }), 400

    created_receipt = ReceiptDBService.insert(receipt)
    return jsonify(created_receipt)


@resources.route('/api/receipts/<int:id_receipt>', methods=['PUT'])
@jwt_required
@admin_required
def update_receipt(id_receipt):
    current_app.logger.debug('In PUT /api/receipts/<int:id_receipt>')

    posted_receipt_data = request.get_json()
    posted_receipt_data['id_r'] = id_receipt

    validation_errors = ReceiptValidationService.validate_post(posted_receipt_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    posted_receipt = ReceiptSchema(only=('id_r', 'id_f', 'montant_r', 'annee_r')).load(posted_receipt_data)
    receipt = Receipt(**posted_receipt)

    # check if receipt exists
    existing_receipt = ReceiptDBService.get_receipt_by_id(id_receipt)
    if not existing_receipt:
        return jsonify({
            'status': 'error',
            'type': 'Not found error',
            'code': 'RECEIPT_NOT_FOUND',
            'message': f'The receipt with id {id_receipt} does not exist'
        }), 404

    # check funding
    FundingDBService.check_funding_exists(existing_receipt['id_f'])

    # check it is the same financement
    if 'id_f' in existing_receipt \
            and existing_receipt['id_f'] is not receipt.id_f:
        return jsonify({
            'status': 'error',
            'type': '',
            'code': 'DIFFERENT_FUNDING',
            'message': f"Cannot change funding while updating receipt. Original funding was {existing_receipt['id_f']},"
                       f" provided is {id_receipt}"
        }), 400

    updated_receipt = ReceiptDBService.update(receipt)
    return jsonify(updated_receipt)


@resources.route('/api/receipts/<int:id_receipt>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_receipt(id_receipt):
    current_app.logger.debug('In DELETE /api/receipts/<int:id_receipt>')

    # check if receipt exists
    existing_receipt = ReceiptDBService.get_receipt_by_id(id_receipt)
    if not existing_receipt:
        return jsonify({
            'status': 'error',
            'type': 'Not found error',
            'code': 'RECEIPT_NOT_FOUND',
            'message': f'The receipt with id {id_receipt} does not exist'
        }), 404

    # check if project status is 'SOLDE'
    if ReceiptDBService.is_project_solde(id_receipt):
        return jsonify({
            'status': 'error',
            'type': 'Receipt project not closed',
            'code': 'RECEIPT_PROJECT_CLOSED',
            'message': f'The receipt with id {id_receipt} cannot be deleted. The associated project is closed'
        }), 400

    # delete the receipt
    id_deleted = ReceiptDBService.delete(id_receipt)
    return jsonify({
        'message': f'Receipt identified by {id_deleted} has been deleted'
    }), 204
