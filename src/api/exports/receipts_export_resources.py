from datetime import datetime

from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import DEFAULT_RECEIPTS_HEADER, export_receipt_item_from_row_proxy, \
    write_fundings_to_google_docs
from src.api.exports.validation_service import ExportValidationService
from src.api.users.auth_resources import admin_required

resources = Blueprint('exports_receipts', __name__)


@resources.route('/api/export/receipts', methods=['POST'])
@jwt_required
@admin_required
def export_receipets():
    current_app.logger.debug('In POST /api/export/receipts')

    post_data = request.get_json()

    validation_errors = ExportValidationService.validate_receipts(post_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occurred',
            'errors': validation_errors
        }), 422

    annee_ref = post_data['annee_ref']

    # default values
    header_column_names = DEFAULT_RECEIPTS_HEADER
    shares = [{'email': get_jwt_identity(), 'type': 'user', 'permission': 'writer'}]
    file_name = f'Export recettes année {annee_ref} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}'

    # overrides if available
    if 'entete' in post_data:
        header_column_names = post_data['entete']
    if 'partages' in post_data:
        shares = post_data['partages']
    if 'nom_fichier' in post_data:
        file_name = post_data['nom_fichier']

    result = ExportDBService.get_bilan_financier(annee_ref)

    if not result:
        return jsonify({
            'message': 'Error while getting fundings to export',
            'type': 'EXPORT',
            'code': 'GET_FUNDING_EXPORT_ERROR',
            'status': 'error'
        }), 500

    export_data = []
    for res in result:
        export_data.append(export_receipt_item_from_row_proxy(res))

    if not len(export_data):
        return jsonify({
            'message': 'No data to export',
            'title': None,
            'lines': 0,
            'url': None,
            'shares': None,
            'annee_ref': annee_ref,
        }), 200

    document_created = write_fundings_to_google_docs(file_name, header_column_names, export_data, shares)

    if not document_created:
        return jsonify({
            'message': 'Error while Google sheet document creation',
            'status': 'error',
            'type': 'EXPORT',
            'code': 'EXPORT_V1_ERROR'
        }), 500

    return jsonify({
        'message': 'successfully created google sheet',
        'title': document_created['title'],
        'lines': document_created['lines'],
        'url': document_created['url'],
        'shares': shares,
        'annee_ref': annee_ref,
    }), 200
