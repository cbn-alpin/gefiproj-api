from flask import Blueprint, current_app, jsonify, request, Response
from .db_services import ReceiptDBService

resources = Blueprint('receipts', __name__)


@resources.route('/api/funding/<int:funding_id>/receipts', methods=['GET'])
def get_receipt_by_funding(funding_id):
    response = Response()
    try:
        current_app.logger.debug('In GET /api/funding/<int:funding_id>/receipts')
        # Checks
        ReceiptDBService.check_funding_exists(funding_id)  
        response = ReceiptDBService.get_receipt_by_funding(funding_id)
        print('coucou 3', response)
    except ValueError as error:
        response = Response(str(error.args[0]),status=error.args[1])
    except Exception as error:
        response.data = str(error)
        response.status_code = 400
    finally:
        return response