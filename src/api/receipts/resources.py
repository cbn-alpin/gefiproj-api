from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from .db_services import ReceiptDBService
from .entities import ReceiptSchema, Receipt
from .validation_service import ReceiptValidationService
from ..fundings.db_services import FundingDBService
from ..users.auth_resources import admin_required

resources = Blueprint('receipts', __name__)


@resources.route('/api/funding/<int:funding_id>/receipts', methods=['GET'])
def get_receipts_by_funding(funding_id):
    try:
        current_app.logger.debug('In GET /api/funding/<int:funding_id>/receipts')
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
    # to be linked to a funding
    current_app.logger.debug('In POST /api/receipts')
    posted_receipt_data = request.get_json()

    validation_errors = ReceiptValidationService.validate_post(posted_receipt_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    posted_receipt = ReceiptSchema(only=('id_f', 'montant_r', 'annee_r')).load(posted_receipt_data)
    receipt = Receipt(**posted_receipt)

    # check funding
    FundingDBService.check_funding_exists(receipt.id_f)

    created_receipt = ReceiptDBService.insert(receipt)
    return jsonify(created_receipt)
