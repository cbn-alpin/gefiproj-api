from flask import Blueprint, current_app, jsonify, request
from shared.entity import Session

from .entities import UserSchema, User

resources = Blueprint('users', __name__)


@resources.route('/auth/register', methods=['POST'])
def add_user():
    current_app.logger.debug('In POST /auth/register')
    posted_user = UserSchema(only=('nom_u', 'prenom_u', 'email_u', 'initiales_u', 'password_u')) \
        .load(request.get_json())
    user = User(**posted_user)

    # hash password

    session = Session()
    session.add(user)
    session.commit()

    new_user = UserSchema().dump(user)
    return jsonify(new_user), 201


@resources.route('/api/users', methods=['GET'])
def get_all_users():
    current_app.logger.debug('In GET /api/users')
    session = Session()
    users_objects = session.query(User).all()

    schema = UserSchema(many=True)
    users = schema.dump(users_objects)

    session.close()
    return jsonify(users)


@resources.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.debug('In GET /api/users/<int:descId>')

    check_user_exists(user_id)

    session = Session()
    user_object = session.query(User).filter_by(id=user_id).first()

    # Transforming into JSON-serializable objects
    schema = UserSchema(many=False)
    description = schema.dump(user_object)

    # Serializing as JSON
    session.close()
    return jsonify(description)


@resources.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    current_app.logger.debug('In PUT /api/users/<int:descId>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = user_id

    # Check if user exists
    check_user_exists(user_id)

    data = UserSchema(only=('id', 'nom', 'prenom', 'mail', 'login', 'password')) \
        .load(data)
    user = User(**data)

    session = Session()
    session.merge(user)
    session.commit()

    updated_user = UserSchema().dump(user)
    session.close()
    return jsonify(updated_user), 200


def check_user_exists(user_id):
    try:
        session = Session()
        existing_user = session.query(User).filter_by(id=user_id).first()
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
