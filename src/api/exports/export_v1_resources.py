# https://www.postgresqltutorial.com/postgresql-python/call-stored-procedures/
# https://gspread.readthedocs.io/en/latest/index.html
# https://medium.com/better-programming/integrating-google-sheets-api-with-python-flask-987d48b7674e
from flask import current_app, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import write_to_google_docs, export_funding_item_from_row_proxy, DEFAULT_HEADER
from src.api.exports.validation_service import ExportValidationService
from src.api.users.auth_resources import admin_required

resources = Blueprint('exports', __name__)


@resources.route('/api/export/fundings/v1', methods=['POST'])
@jwt_required
@admin_required
def export_fundings_v1():
    current_app.logger.debug('In POST /api/export/fundings/v1')

    post_data = request.get_json()

    validation_errors = ExportValidationService.validate_v1(post_data)
    if len(validation_errors) > 0:
        return jsonify(), 422

    annee_ref = post_data['annee_ref']
    shares = post_data['partages']
    header_column_names = DEFAULT_HEADER
    if 'entete' in post_data:
        header_column_names = post_data['entete']

    result = ExportDBService.get_suivi_financement(1, annee_ref)

    if not result:
        return jsonify({
            'status': 'Error while getting fundings'
        }), 500

    export_data = []
    for res in result:
        export_data.append(export_funding_item_from_row_proxy(res))

    if not len(export_data):
        return jsonify({'message': 'No data to export'}), 200

    document_created = write_to_google_docs('', header_column_names, export_data, shares)

    if not document_created:
        return jsonify({
            'message': 'Error while Google sheet document creation',
            'status': 'error',
            'type': 'EXPORT',
            'code': 'EXPORT_V1_ERROR'
        }), 500

    return jsonify({
        'message': 'successfully created google sheet',
        'title': document_created.title,
        'lines': document_created.lines
    }), 200  # TODO: Return the url of created doc
