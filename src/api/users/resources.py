from flask import Blueprint, current_app, jsonify, request
from shared.entity import Session

from .entities import UserSchema, User

resources = Blueprint('users', __name__)


@resources.route('/auth/register', methods=['POST'])
def add_user():
    current_app.logger.debug('In POST /auth/register')
    posted_user = UserSchema(only=('nom', 'prenom', 'mail', 'login', 'password')) \
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


@resources.route('/api/users/<int:userId>', methods=['GET'])
def get_user_by_id(userId):
    current_app.logger.debug('In GET /api/users/<int:descId>')

    session = Session()
    user_object = session.query(User).filter_by(id=userId).first()

    # Transforming into JSON-serializable objects
    schema = UserSchema(many=False)
    description = schema.dump(user_object)

    # Serializing as JSON
    session.close()
    return jsonify(description)


@resources.route('/api/users/<int:userId>', methods=['PUT'])
def update_user(userId):
    current_app.logger.debug('In PUT /api/users/<int:descId>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = userId

    # Check if user exists

    data = UserSchema(only=('id', 'nom', 'prenom', 'mail', 'login', 'password')) \
        .load(data)
    user = User(**data)

    session = Session()
    session.merge(user)
    session.commit()

    updated_user = UserSchema().dump(user)
    session.close()
    return jsonify(updated_user), 200
