from flask import Blueprint, jsonify

resources = Blueprint('status', __name__)


@resources.route('/status', methods=['GET'])
def get_status():
    return jsonify('ok')
