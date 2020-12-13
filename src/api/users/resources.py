from functools import wraps

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, verify_jwt_in_request, \
    get_jwt_claims
from sqlalchemy.orm import subqueryload

from src.shared.entity import Session
from .db_services import UserDBService
from .entities import UserSchema, User

resources = Blueprint('users', __name__)


@resources.route('/api/auth/register', methods=['POST'])
def add_user():
    current_app.logger.debug('In POST /api/auth/register')
    posted_user = UserSchema(only=('nom_u', 'prenom_u', 'email_u', 'initiales_u', 'active_u', 'password_u')) \
        .load(request.get_json())
    user = User(**posted_user)

    # check if user exists by initiales and email

    session = Session()
    session.add(user)
    session.commit()

    new_user = UserSchema().dump(user)
    return jsonify(new_user), 201


@resources.route('/api/auth/login', methods=['POST'])
def login():
    current_app.logger.debug('In POST /api/auth/login')

    data = request.get_json()

    current_user = User.find_by_login(data['login'])
    if not current_user:
        return {'message': 'User {} doesn\'t exist'.format(data['login'])}, 404

    if User.verify_hash(data['password'], current_user.password_u):
        roles = UserDBService.get_user_role_names_by_user_id(current_user.id_u)
        print(f'user id is {current_user.id_u}')
        print(roles)
        identity = {
            'login': data['login'],
            'roles': roles
        }
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        return {
            'id_u': current_user.id_u,
            'nom_u': current_user.nom_u,
            'prenom_u': current_user.prenom_u,
            'initiales_u': current_user.initiales_u,
            'email_u': current_user.email_u,
            'roles': roles,
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
        .options(subqueryload(User.roles)).filter_by(id_u=user_id).first()

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


# Here is a custom decorator that verifies the JWT is present in
# the request, as well as insuring that this user has a role of
# `admin` in the access token
# https://stackoverflow.com/questions/33597150/using-flask-security-roles-with-flask-jwt-rest-api
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper
