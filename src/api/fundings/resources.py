from flask import Blueprint, current_app, jsonify, request, Response
from .db_services import FundingDBService

resources = Blueprint('funding', __name__)


@resources.route('/api/projects/<int:project_id>/fundings', methods=['GET'])
def get_fundings_by_project(project_id):
    response = Response()
    try:
        current_app.logger.debug('In GET /api/projects/<int:project_id>/fundings')
        # Checks
        FundingDBService.check_project_exists(project_id)  
        response = FundingDBService.get_funding_by_projects(project_id)
    except ValueError as error:
        response = Response(str(error.args[0]),status=error.args[1])
    except Exception as error:
        response.data = str(error)
        response.status_code = 400
    finally:
        return response


@resources.route('/api/funding', methods=['POST'])
# @requires_auth
def add_funding():
    response = Response()
    try:
        current_app.logger.debug('In POST /api/funding')
        # Load data
        posted_funding = request.get_json()
        # Checks
        FundingDBService.check_project_exists(posted_funding['id_p'])
        response = FundingDBService.insert_funding(posted_funding)
    except ValueError as error:
        response = Response(str(error.args[0]),status=error.args[1])
    except Exception as error:
        response.data = str(error)
        response.status_code = 400
    finally:
        return response


@resources.route('/api/funding/<int:funding_id>', methods=['PUT'])
# @requires_auth
def update_funding(funding_id):
    response = Response()
    try:
        current_app.logger.debug('In PUT /api/funding/<int:funding_id>')
        # Load data
        data = request.get_json()
        if 'id_f' not in data:
            data['id_f'] = funding_id
        # Checks
        FundingDBService.check_funding_exists(data['id_f'])
        reponse = FundingDBService.update_funding(data)
    except ValueError as error:
        response = Response(str(error.args[0]),status=error.args[1])
    except Exception as error:
        response.data = str(error)
        response.status_code = 400
    finally:
        return response


@resources.route('/api/funding/<int:funding_id>', methods=['DELETE'])
# @requires_role('admin')
def delete_funding(funding_id):
    response = Response()
    try:
        # check
        FundingDBService.check_funding_exists(funding_id)
        response = FundingDBService.delete_funding(funding_id)
    except ValueError as error:
        response = Response(str(error.args[0]),status=error.args[1])
    except Exception as error:
        response.data = str(error)
        response.status_code = 400
    finally:
        return response