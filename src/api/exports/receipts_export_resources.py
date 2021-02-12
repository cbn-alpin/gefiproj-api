from datetime import datetime

from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required

from src.api.exports.basic_formatting import basic_formatting_receipt
from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import export_receipt_item_from_row_proxy, \
    write_rececipts_to_google_docs, generate_header_first_tab_0, get_max_year, \
    get_all_year_in_result, create_real_data_export
from src.api.exports.validation_service import ExportValidationService

resources = Blueprint('exports_receipts', __name__)


@resources.route('/api/export/receipts', methods=['POST'])
@jwt_required
def export_receipets():
    current_app.logger.debug('In POST /api/export/receipts')

    post_data = request.get_json()

    validation_errors = ExportValidationService.validate_receipts(post_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'Une erreur est survenue lors de la validation des données',
            'errors': validation_errors
        }), 422

    annee_ref = post_data['annee_ref']

    file_name = f'Export recettes année {annee_ref} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}'

    result = ExportDBService.get_bilan_financier(annee_ref)

    if not result:
        return jsonify({
            'message': 'Une erreur est survenue lors de l\'export des financements',
            'type': 'EXPORT',
            'code': 'GET_FUNDING_EXPORT_ERROR',
            'status': 'error'
        }), 500

    export_data = []
    for res in result:
        export_data.append(export_receipt_item_from_row_proxy(res))

    if not len(export_data):
        return jsonify({
            'message': 'Aucune donnée à exporter',
            'title': None,
            'lines': 0,
            'url': None,
            'shares': None,
            'annee_ref': annee_ref,
        }), 200

    # get max year
    annee_max = get_max_year(annee_ref, export_data)
    # default values
    header_column_names = generate_header_first_tab_0(annee_ref)

    current_year_range = get_all_year_in_result(export_data)
    new_export_data = create_real_data_export(current_year_range, annee_ref, annee_max, export_data)

    document_created = write_rececipts_to_google_docs(file_name, header_column_names, new_export_data)

    # return jsonify(document_created)

    if not document_created:
        return jsonify({
            'message': 'Une erreur est survenue lors de la création du document Google sheet',
            'status': 'error',
            'type': 'EXPORT',
            'code': 'EXPORT_V1_ERROR'
        }), 500

    # basic formatting
    basic_formatting_receipt(document_created['session'], document_created['spreadsheetId'], annee_ref,
                             len(new_export_data))

    return jsonify({
        'message': 'Le document Google Sheet a été crée avec succès',
        # 'spreadsheetId': document_created['spreadsheetId'],
        # 'session': document_created['session'],
        # 'title': document_created['title'],
        # 'lines': document_created['lines'],
        'url': document_created['url'],
        # 'shares': shares,
        'annee_ref': annee_ref,
    }), 200
