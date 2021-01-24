from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import jwt_required

from src.shared.entity import Session
from .entities import RoleAccess, RoleAccessSchema

resources = Blueprint('role_access', __name__)


@resources.route('/api/role_access', methods=['GET'])
@jwt_required
def get_all_role_acces():
    current_app.logger.info('In GET /role_access')
    # Fetching from the database
    session = Session()
    role_access_objects = session.query(RoleAccess).all()

    # Transforming into JSON-serializable objects
    schema = RoleAccessSchema(many=True)
    role_access = schema.dump(role_access_objects)

    # Serializing as JSON
    session.close()
    return jsonify(role_access)
