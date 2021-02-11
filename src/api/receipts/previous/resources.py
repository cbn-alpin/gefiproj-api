import json

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

from src.api.users.auth_resources import admin_required
from .db_services import InputOutputDBService
from .entities import InputOutput, InputOutputSchema
from .validation_service import InputOutputValidationService

resources = Blueprint('receipts_previous', __name__)


@resources.route('/api/receipts/previous/<int:input_output_id>', methods=['GET'])
@jwt_required
@admin_required
def get_input_output(input_output_id):
    try:
        current_app.logger.debug('In GET /api/receipts/previous/<int:input_output_id>')
        # Checks
        # check if input_output exists
        InputOutputDBService.check_input_output_exists(input_output_id)

        response = InputOutputDBService.get_input_output_by_id(input_output_id)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous', methods=['GET'])
@jwt_required
def get_input_output_by_filter():
    try:
        current_app.logger.debug('In GET /api/receipts/previous')
        query_param = request.args
        if len(query_param) == 0:
            response = InputOutputDBService.get_input_output_by_filter()  # No filter
        else:
            response = InputOutputDBService.get_input_output_by_filter(query_param)

        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous', methods=['POST'])
@jwt_required
@admin_required
def add_input_output():
    try:
        current_app.logger.debug('In POST /api/receipts/previous')
        posted_input_output = request.get_json()
        InputOutputValidationService.validate_post(posted_input_output)
        posted_input_output = InputOutputSchema(only=('annee_recette_es', 'annee_affectation_es', 'montant_es')).load(
            posted_input_output, unknown=EXCLUDE)
        input_output = InputOutput(**posted_input_output)

        # check if new input_output unique
        InputOutputDBService.check_input_output_uniqueness(input_output.annee_recette_es,
                                                           input_output.annee_affectation_es)
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

        InputOutputValidationService.validate_post(posted_input_output)

        posted_input_output = InputOutputSchema(
            only=('id_es', 'annee_recette_es', 'annee_affectation_es', 'montant_es')).load(posted_input_output,
                                                                                           unknown=EXCLUDE)
        input_output = InputOutput(**posted_input_output)

        # check if input_output exists
        InputOutputDBService.check_input_output_exists(input_output_id)

        # check if new input_output unique
        InputOutputDBService.check_input_output_uniqueness(input_output.annee_recette_es,
                                                           input_output.annee_affectation_es,
                                                           input_output_id)

        updated_input_output = InputOutputDBService.update(input_output)
        return jsonify(updated_input_output), 200

    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/receipts/previous/<int:id_input_output>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_input_output(id_input_output):
    try:
        current_app.logger.debug('In DELETE /api/receipts/previous/<int:id_input_output>')

        # check if input_output exists
        InputOutputDBService.check_input_output_exists(id_input_output)

        # delete the input_output
        id_deleted = InputOutputDBService.delete(id_input_output)
        message = '{"message" : "Entrée sorties {' + str(id_deleted) + '} a été supprimée."}'
        return json.loads(message), 204

    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
