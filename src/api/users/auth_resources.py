from functools import wraps

from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    verify_jwt_in_request, get_jwt_claims, decode_token, jwt_required

from src.api.users.db_services import UserDBService
from src.api.users.entities import User, UserSchema
from .validation_service import UserValidationService
from .. import jwt

resources = Blueprint('auth', __name__)


# https://stackoverflow.com/questions/33597150/using-flask-security-roles-with-flask-jwt-rest-api
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'administrateur' not in claims['roles']:
            return jsonify(msg='This operation is permitted to admins only!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


@resources.route('/api/auth/login', methods=['POST'])
def login():
    current_app.logger.debug('In POST /api/auth/login')

    data = request.get_json()

    user = User.find_by_login(data['login'])
    if not user:
        return {'message': 'User {} doesn\'t exist'.format(data['login'])}, 404

    if User.verify_hash(data['password'], user.password_u):
        identity = data['login']
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        return {
            'id_u': user.id_u,
            'nom_u': user.nom_u,
            'prenom_u': user.prenom_u,
            'initiales_u': user.initiales_u,
            'email_u': user.email_u,
            'roles': decode_token(access_token)['user_claims']['roles'],
            'active_u': user.active_u,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    else:
        return {'message': 'Wrong credentials'}


@resources.route('/api/auth/register', methods=['POST'])
@jwt_required
@admin_required
def add_user():
    current_app.logger.debug('In POST /api/auth/register')
    posted_user = UserSchema(only=('nom_u', 'prenom_u', 'email_u', 'initiales_u', 'active_u', 'password_u')) \
        .load(request.get_json())

    # validate user posted data
    validation_errors = UserValidationService.validate_post(posted_user)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    user = User(**posted_user)

    # check if user exists by initiales and email
    user_by_email = UserDBService.get_user_by_email(user.email_u)
    user_by_initiales = UserDBService.get_user_by_initiales(user.initiales_u)
    if user_by_email or user_by_initiales:
        if user_by_email:
            return jsonify({'message': 'A user with email {} is already in use'.format(user.email_u)}), 409
        return jsonify({'message': 'A user with initials {} is already in use'.format(user.initiales_u)}), 409

    new_user = UserDBService.insert_user(user)
    return jsonify(new_user), 201


@resources.route('/api/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_app.logger.debug('In POST /api/auth/refresh')
    user_identity = get_jwt_identity()
    new_token = {
        'access_token': create_access_token(identity=user_identity)
    }
    return jsonify(new_token), 200


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    roles = UserDBService.get_user_role_names_by_user_id_or_email(identity)
    return {'roles': roles}
