from datetime import datetime

from flask import current_app, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.exports.basic_formatting import delete_column_by_index, \
    basic_formatting_funding
from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import export_funding_item_from_row_proxy, write_fundings_to_google_docs, \
    DEFAULT_FUNDINGS_HEADER, create_right_header_title_bilan_1
from src.api.exports.validation_service import ExportValidationService

resources = Blueprint('exports_fundings', __name__)


@resources.route('/api/export/fundings', methods=['POST'])
@jwt_required
def export_fundings():
    current_app.logger.debug('In POST /api/export/fundings')

    post_data = request.get_json()

    validation_errors = ExportValidationService.validate(post_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'Une erreur est survenue lors de la validation des données',
            'errors': validation_errors
        }), 422

    version = post_data['version']
    annee_ref = post_data['annee_ref']

    # default values
    annee_max = 0

    shares = [{'email': get_jwt_identity(), 'type': 'user', 'permission': 'writer'}]

    # overrides if available
    if 'partages' in post_data:
        shares = post_data['partages']
    if 'nom_fichier' in post_data:
        file_name = post_data['nom_fichier']
    if 'annee_max' in post_data and version == 2:
        annee_max = post_data['annee_max']

    if version == 2:
        file_name = f'Export financement année {annee_ref} | {annee_max} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}'
    else:
        file_name = f'Export financement année {annee_ref} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}'

    result = ExportDBService.get_suivi_financement(version, annee_ref, annee_max)

    if not result:
        return jsonify({
            'message': 'Une erreur est survenue lors de l\'export des financements',
            'type': 'EXPORT',
            'code': 'GET_FUNDING_EXPORT_ERROR',
            'status': 'error'
        }), 500

    export_data = []
    for res in result:
        export_data.append(export_funding_item_from_row_proxy(res))

    if not len(export_data):
        return jsonify({
            'message': 'Aucune donnée à exporter',
            'title': None,
            'lines': 0,
            'url': None,
            'shares': None,
            'annee_ref': annee_ref,
            'annee_max': annee_max,
            'version': version,
        }), 200

    header_column_names = create_right_header_title_bilan_1(annee_ref)

    document_created = write_fundings_to_google_docs(file_name, header_column_names, export_data, shares)

    if not document_created:
        return jsonify({
            'message': 'Une erreur est survenue lors de la création du document Google sheet',
            'status': 'error',
            'type': 'EXPORT',
            'code': 'EXPORT_V1_ERROR'
        }), 500

    # Before send data to front
    # make some conditional format
    # conditional_formatting_funding(document_created['session'], document_created['spreadsheetId'], document_created['lines'])
    basic_formatting_funding(document_created['session'], document_created['spreadsheetId'], export_data)

    # delete last column
    delete_column_by_index(document_created['session'], document_created['spreadsheetId'], 14)

    return jsonify({
        'message': 'Le document Google Sheet a été crée avec succès',
        'title': document_created['title'],
        'lines': document_created['lines'],
        'url': document_created['url'],
        # 'spreadsheetId': document_created['spreadsheetId'],
        # 'session': document_created['session'],
        # 'spreadsheetId': document_created['spreadsheetId'],
        # 'shares': shares,
        'annee_ref': annee_ref,
        'annee_max': annee_max,
        'version': version,
    }), 200
