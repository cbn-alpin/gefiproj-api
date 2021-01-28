from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import subqueryload

from src.shared.entity import Session
from .auth_resources import admin_required
from .db_services import UserDBService
from .entities import UserSchema, User

resources = Blueprint('users', __name__)


@resources.route('/api/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    current_app.logger.debug('In GET /api/users')
    session = Session()
    users_objects = session.query(User) \
        .with_entities(User.id_u, User.nom_u, User.prenom_u, User.initiales_u, User.email_u, User.active_u) \
        .all()

    schema = UserSchema(many=True)
    users = schema.dump(users_objects)

    session.close()
    return jsonify(users)


@resources.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id):
    current_app.logger.debug('In GET /api/users/<int:descId>')

    check_user_exists_by_id(user_id)

    session = Session()
    user_object = session.query(User) \
        .with_entities(User.id_u, User.nom_u, User.prenom_u, User.initiales_u, User.email_u, User.active_u) \
        .options(subqueryload(User.roles)).filter_by(id_u=user_id).first()

    # Transforming into JSON-serializable objects
    schema = UserSchema(many=False)
    user = schema.dump(user_object)

    # Serializing as JSON
    session.close()
    return jsonify(user)


@resources.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_user(user_id):
    current_app.logger.debug('In PUT /api/users/<int:descId>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = user_id

    # Check if user exists
    exist_error = UserDBService.check_user_exists_by_id(user_id)
    if exist_error is not None:
        return jsonify(exist_error), 404

    data = UserSchema(only=('nom_u', 'prenom_u', 'email_u', 'initiales_u', 'password_u')) \
        .load(data)
    user = User(**data)

    session = Session()
    session.merge(user)
    session.commit()

    updated_user = UserSchema().dump(user)
    session.close()
    return jsonify(updated_user), 200


def check_user_exists_by_id(user_id):
    try:
        session = Session()
        existing_user = session.query(User).filter_by(id_u=user_id).first()
        session.close()

        if existing_user is None:
            raise ValueError('This user does not exist')
    except ValueError:
        resp = jsonify({"error": {
            'code': 'USER_NOT_FOUND',
            'message': f'User with id {user_id} does not exist.'
        }})
        resp.status_code = 404
        return resp
