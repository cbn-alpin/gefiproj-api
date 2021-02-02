from datetime import datetime

from flask import current_app, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import write_to_google_docs, export_funding_item_from_row_proxy, DEFAULT_HEADER
from src.api.exports.validation_service import ExportValidationService
from src.api.users.auth_resources import admin_required

resources = Blueprint('exports', __name__)


@resources.route('/api/export/fundings', methods=['POST'])
@jwt_required
@admin_required
def export_fundings():
    current_app.logger.debug('In POST /api/export/fundings')

    post_data = request.get_json()

    validation_errors = ExportValidationService.validate(post_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    version = post_data['version']
    annee_ref = post_data['annee_ref']

    # default values
    annee_max = 0
    header_column_names = DEFAULT_HEADER
    shares = get_jwt_identity()
    file_name = f'Export financement année {annee_ref} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}'

    # overrides if available
    if 'partages' in post_data:
        shares = post_data['partages']
    if 'entete' in post_data:
        header_column_names = post_data['entete']
    if 'nom_fichier' in post_data:
        file_name = post_data['nom_fichier']
    if 'annee_max' in post_data and version == 2:
        annee_max = post_data['annee_max']

    result = ExportDBService.get_suivi_financement(version, annee_ref, annee_max)

    if not result:
        return jsonify({
            'message': 'Error while getting fundings to export',
            'type': 'EXPORT',
            'code': 'GET_FUNDING_EXPORT_ERROR',
            'status': 'error'
        }), 500

    export_data = []
    for res in result:
        export_data.append(export_funding_item_from_row_proxy(res))

    if not len(export_data):
        return jsonify({
            'message': 'No data to export',
            'title': None,
            'lines': 0,
            'url': None,
            'shares': None,
            'annee_ref': annee_ref,
            'annee_max': annee_max,
            'version': version,
        }), 200

    document_created = write_to_google_docs(file_name, header_column_names, export_data, shares)

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
        'annee_max': annee_max,
        'version': version,
    }), 200
