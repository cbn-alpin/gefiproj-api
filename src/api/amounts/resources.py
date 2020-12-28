from flask import Blueprint, current_app, jsonify, request, Response
from .db_services import AmountDBService

resources = Blueprint('amounts', __name__)


@resources.route('/api/receipt/<int:receipt_id>/amounts', methods=['GET'])
def get_amounts_by_receipt(receipt_id):
    try:
        current_app.logger.debug('In GET /api/receipt/<int:receipt_id>/amounts')
        # Checks
        AmountDBService.check_receipt_exists(receipt_id)  
        response = AmountDBService.get_amount_by_receipt_(receipt_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]