from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

from .db_services import ReceiptDBService, InputOutputDBService
from .entities import ReceiptSchema, Receipt, InputOutput, InputOutputSchema
from .validation_service import ReceiptValidationService, InputOutputValidationService
from ..amounts.db_services import AmountDBService
from ..fundings.db_services import FundingDBService
from ..users.auth_resources import admin_required
import json

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


@resources.route('/api/receipts', methods=['POST'])
@jwt_required
def add_receipt():
    current_app.logger.debug('In POST /api/receipts')
    posted_receipt_data = request.get_json()

    validation_errors = ReceiptValidationService.validate_post(posted_receipt_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occurred',
            'errors': validation_errors
        }), 422

    posted_receipt = ReceiptSchema(only=('id_f', 'montant_r', 'annee_r')).load(posted_receipt_data, unknown=EXCLUDE)
    receipt = Receipt(**posted_receipt)

    # check funding
    FundingDBService.get_funding_by_id(receipt.id_f)

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
            'message': 'A validation error occurred',
            'errors': validation_errors
        }), 422

    posted_receipt = ReceiptSchema(only=('id_r', 'id_f', 'montant_r', 'annee_r')).load(posted_receipt_data,
                                                                                       unknown=EXCLUDE)
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

    # delete children
    AmountDBService.delete_amounts_by_receipt_id(id_receipt)
    # delete the receipt
    id_deleted = ReceiptDBService.delete(id_receipt)
    return jsonify({
        'message': f'Receipt identified by {id_deleted} has been deleted'
    }), 204

@resources.route('/api/receipts/previous/<int:input_output_id>', methods=['GET'])
@jwt_required
def get_input_output(input_output_id):
    try:
        current_app.logger.debug('In GET /api/receipts/previous/<int:input_output_id>')
        # Checks
        # check if input_output exists
        existing_input_output = InputOutputDBService.check_input_output_exists(input_output_id)
        if  existing_input_output is None:
            return jsonify({
                'status': 'error',
                'type': 'Not found error',
                'code': 'INPUT_OUTPUT_NOT_FOUND',
                'message': f'L \'entrée sortie id= {input_output_id} n\'existe pas.'
            }), 404
        response = InputOutputDBService.get_input_output_by_id(input_output_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@resources.route('/api/receipts/previous', methods=['GET'])
@jwt_required
def get_input_output_by_filter():
    try:
        current_app.logger.debug('In GET /api/receipts/previous?properties')
        query_param = request.args
        response = InputOutputDBService.get_input_output_by_filter(query_param)
        if len(response) == 0 :
            return jsonify({
                        'status': 'error',
                        'type': 'Not found error',
                        'code': 'INPUT_OUTPUT_NOT_FOUND',
                        'message': f'Il n\'y a pas d\'entrée sorties satisfaisants vos critères '
                    }), 404
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@resources.route('/api/receipts/previous/all', methods=['GET'])
@jwt_required
def get_all_input_output():
    try:
        current_app.logger.debug('In GET /api/receipts/previous/all')
        response = InputOutputDBService.get_input_output_by_filter() #No filter
        if len(response) == 0 :
            return jsonify({
                        'status': 'error',
                        'type': 'Not found error',
                        'code': 'INPUT_OUTPUT_NOT_FOUND',
                        'message': f'Il n\'y a pas d\'entrée sorties satisfaisants vos critères '
                    }), 404
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous', methods=['POST'])
@jwt_required
@admin_required
def add_input_output():
    current_app.logger.debug('In POST /api/receipts/previous')
    posted_input_output = request.get_json()
    validation_errors = InputOutputValidationService.validate_post(posted_input_output)

    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occurred',
            'errors': validation_errors
        }), 422

    try:
        posted_input_output = InputOutputSchema(only=('annee_recette_es', 'annee_affectation_es', 'montant_es')).load(posted_input_output, unknown=EXCLUDE)
        input_output = InputOutput(**posted_input_output)

        # check if new input_output unique
        unique_input_output = InputOutputDBService.check_input_output_uniqueness(input_output.annee_recette_es, input_output.annee_affectation_es)
        if  unique_input_output is not None:
            return jsonify({
                'status': 'error',
                'type': 'Not found error',
                'code': 'INPUT_OUTPUT_UNIQUE_VIOLATION',
                'message': f'L entree sortie ({input_output.annee_recette_es} , {input_output.annee_affectation_es}) existe déjà.'
            }), 400

        created_input_output = InputOutputDBService.insert(input_output)
        return jsonify(created_input_output), 201

    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous/<int:input_output_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_input_output(input_output_id):
    try:
        current_app.logger.debug('In PUT /api/receipts/previous/<int:input_output_id>')

        posted_input_output = request.get_json()
        posted_input_output['id_es'] = input_output_id

        validation_errors = InputOutputValidationService.validate_post(posted_input_output)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occurred',
                'errors': validation_errors
            }), 422

        posted_input_output = InputOutputSchema(only=('id_es', 'annee_recette_es', 'annee_affectation_es', 'montant_es')).load(posted_input_output, unknown=EXCLUDE)
        input_output = InputOutput(**posted_input_output)

        # check if input_output exists
        existing_input_output = InputOutputDBService.check_input_output_exists(input_output_id)
        if  existing_input_output is None:
            return jsonify({
                'status': 'error',
                'type': 'Not found error',
                'code': 'INPUT_OUTPUT_NOT_FOUND',
                'message': f'L \'entrée sortie id= {input_output_id} n\'existe pas.'
            }), 404

        # check if new input_output unique
        unique_input_output = InputOutputDBService.check_input_output_uniqueness(input_output.annee_recette_es, input_output.annee_affectation_es,input_output_id)
        if  unique_input_output is not None:
            return jsonify({
                'status': 'error',
                'type': 'Not found error',
                'code': 'INPUT_OUTPUT_UNIQUE_VIOLATION',
                'message': f'L entree sortie ({input_output.annee_recette_es} , {input_output.annee_affectation_es}) existe déjà.'
            }), 400

        updated_input_output = InputOutputDBService.update(input_output)
        return jsonify(updated_input_output) , 200

    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous/<int:id_input_output>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_input_output(id_input_output):
    try:
        current_app.logger.debug('In DELETE /api/receipts/previous/<int:id_input_output>')

        # check if input_output exists
        existing_input_output = InputOutputDBService.check_input_output_exists(id_input_output)
        if  existing_input_output is None:
            return jsonify({
                'status': 'error',
                'type': 'Not found error',
                'code': 'INPUT_OUTPUT_NOT_FOUND',
                'message': f'L\'entrée sorties {id_input_output} n\'existe pas.'
            }), 404

        # delete the input_output
        id_deleted = InputOutputDBService.delete(id_input_output)
        message = '{"message" : "Entrée sorties {'+str(id_deleted)+'} a été supprimée."}'
        return json.loads(message) , 204

    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]