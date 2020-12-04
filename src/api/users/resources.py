from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from shared.entity import Session

from .entities import UserSchema, User

resources = Blueprint('users', __name__)


@resources.route('/auth/register', methods=['POST'])
def add_user():
    current_app.logger.debug('In POST /auth/register')
    posted_user = UserSchema(only=('nom_u', 'prenom_u', 'email_u', 'initiales_u', 'active_u', 'password_u')) \
        .load(request.get_json())
    user = User(**posted_user)

    # check if user exists by initiales and email

    session = Session()
    session.add(user)
    session.commit()

    new_user = UserSchema().dump(user)
    return jsonify(new_user), 201


@resources.route('/auth/login', methods=['POST'])
def login():
    current_app.logger.debug('In POST /auth/login')

    data = request.get_json()

    current_user = User.find_by_login(data['login'])
    if not current_user:
        return {'message': 'User {} doesn\'t exist'.format(data['login'])}, 404

    if User.verify_hash(data['password'], current_user.password_u):
        access_token = create_access_token(identity=data['login'])
        refresh_token = create_refresh_token(identity=data['login'])

        return {
            'id_u': current_user.id_u,
            'nom_u': current_user.nom_u,
            'prenom_u': current_user.prenom_u,
            'initiales_u': current_user.initiales_u,
            'email_u': current_user.email_u,
            'active_u': current_user.active_u,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    else:
        return {'message': 'Wrong credentials'}


@resources.route('/api/users', methods=['GET'])
@jwt_required
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
        .filter_by(id_u=user_id).first()

    # Transforming into JSON-serializable objects
    schema = UserSchema(many=False)
    user = schema.dump(user_object)

    # Serializing as JSON
    session.close()
    return jsonify(user)


@resources.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    current_app.logger.debug('In PUT /api/users/<int:descId>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = user_id

    # Check if user exists
    check_user_exists_by_id(user_id)

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
