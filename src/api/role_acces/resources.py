from flask import Blueprint, current_app, jsonify, request
from shared.auth import AuthError
from shared.entity import Session

from .entities import RoleAcces, RoleAccesSchema

# Versions infos

resources = Blueprint('role_acces', __name__)


@resources.route('/role_acces', methods=['GET'])
def get_all_role_acces():
    current_app.logger.info('In GET /role_acces')
    # Fetching from the database
    session = Session()
    role_acces_objects = session.query(RoleAcces).all()

    # Transforming into JSON-serializable objects
    schema = RoleAccesSchema(many=True)
    role_acces = schema.dump(role_acces_objects)

    # Serializing as JSON
    session.close()
    return jsonify(role_acces)