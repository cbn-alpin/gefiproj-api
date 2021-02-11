from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

from .db_services import ReceiptDBService
from .entities import ReceiptSchema, Receipt
from .validation_service import ReceiptValidationService
from ..amounts.db_services import AmountDBService
from ..fundings.db_services import FundingDBService
from ..users.auth_resources import admin_required

resources = Blueprint('receipts', __name__)


@resources.route('/api/fundings/<int:funding_id>/receipts', methods=['GET'])
@jwt_required
def get_receipts_by_funding(funding_id):
    try:
        current_app.logger.debug('In GET /api/fundings/<int:funding_id>/receipts')
        # Checks
        ReceiptDBService.check_funding_exists(funding_id)
        response = ReceiptDBService.get_receipts_by_funding_id(funding_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts', methods=['POST'])
@jwt_required
def add_receipt():
    try:
        current_app.logger.debug('In POST /api/receipts')
        posted_receipt_data = request.get_json()

        ReceiptValidationService.validate_post(posted_receipt_data)

        posted_receipt = ReceiptSchema(only=('id_f', 'montant_r', 'annee_r')).load(posted_receipt_data, unknown=EXCLUDE)
        receipt = Receipt(**posted_receipt)

        # check funding
        FundingDBService.get_funding_by_id(receipt.id_f)

        # check there is no receipt for this funding this year
        ReceiptDBService.get_receipts_of_year_by_funding_id(receipt.id_f, receipt.annee_r)

        created_receipt = ReceiptDBService.insert(receipt)
        return jsonify(created_receipt), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/<int:id_receipt>', methods=['PUT'])
@jwt_required
@admin_required
def update_receipt(id_receipt):
    try:
        current_app.logger.debug('In PUT /api/receipts/<int:id_receipt>')

        posted_receipt_data = request.get_json()
        posted_receipt_data['id_r'] = id_receipt

        ReceiptValidationService.validate_post(posted_receipt_data)

        posted_receipt = ReceiptSchema(only=('id_r', 'id_f', 'montant_r', 'annee_r')).load(posted_receipt_data,
                                                                                           unknown=EXCLUDE)
        posted_receipt = Receipt(**posted_receipt)

        # check if receipt exists
        receipt = ReceiptDBService.get_receipt_by_id(id_receipt)

        # check funding
        FundingDBService.get_funding_by_id(posted_receipt.id_f)

        # TODO: check business rule cf. Hanh
        # # check it is the same financement
        # if 'id_f' in existing_receipt \
        #         and existing_receipt['id_f'] is not receipt.id_f:
        #     return jsonify({
        #         'status': 'error',
        #         'type': '',
        #         'code': 'DIFFERENT_FUNDING',
        #         'message': f"Cannot change funding while updating receipt. Original funding was {existing_receipt['id_f']},"
        #                    f" provided is {id_receipt}"
        #     }), 400

        updated_receipt = ReceiptDBService.update(posted_receipt)
        return jsonify(updated_receipt), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/<int:id_receipt>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_receipt(id_receipt):
    try:
        current_app.logger.debug('In DELETE /api/receipts/<int:id_receipt>')

        # check if receipt exists
        ReceiptDBService.get_receipt_by_id(id_receipt)

        # check if project status is 'SOLDE'
        ReceiptDBService.is_project_solde(id_receipt)

        # delete children
        AmountDBService.delete_amounts_by_receipt_id(id_receipt)
        # delete the receipt
        id_deleted = ReceiptDBService.delete(id_receipt)
        return jsonify({
            'message': f'Recette identifié par {id_deleted} à été supprimé'
        }), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]
