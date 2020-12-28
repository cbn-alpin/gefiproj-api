from flask import Blueprint, current_app, jsonify, request, Response
from .db_services import ReceiptDBService

resources = Blueprint('receipts', __name__)


@resources.route('/api/funding/<int:funding_id>/receipts', methods=['GET'])
def get_receipts_by_funding(funding_id):
    try:
        current_app.logger.debug('In GET /api/funding/<int:funding_id>/receipts')
        # Checks
        ReceiptDBService.check_funding_exists(funding_id)  
        response = ReceiptDBService.get_receipts_by_funding(funding_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]