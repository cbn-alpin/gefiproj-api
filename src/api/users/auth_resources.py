from functools import wraps

from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity, \
    verify_jwt_in_request, get_jwt_claims, jwt_required, get_raw_jwt
from .. import jwt

from src.api.users.db_services import UserDBService
from .validation_service import UserValidationService
from src.shared.manage_error import CodeError, ManageErrorUtils, TError
from jwt.exceptions import ExpiredSignatureError

resources = Blueprint('auth', __name__)

# https://stackoverflow.com/questions/33597150/using-flask-security-roles-with-flask-jwt-rest-api
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if 'roles' not in claims or 'administrateur' not in claims['roles']:
                msg = "Cette opération n'est autorisée que pour les adminisatreurs seulement"
                ManageErrorUtils.exception(CodeError.TOKEN_HAS_NOT_ENOUGH_PRIVILEGES, TError.TOKEN_ERROR, msg, 403)
            return fn(*args, **kwargs)

        except (ValueError, Exception) as error:
            current_app.logger.error(error)
            return jsonify(error.args[0]), error.args[1]
    return wrapper
        
        
@resources.route('/api/auth/login', methods=['POST'])
def login():
    current_app.logger.debug('In POST /api/auth/login')
    response = None
    try:
        data = request.get_json()
        UserValidationService.validate_login(data)
        auth = UserDBService.auth_login(data)
        response = jsonify(auth), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response
    

@resources.route('/api/auth/logout', methods=['POST'])
@jwt_required
def logout():
    current_app.logger.debug('In POST /api/auth/logout')
    response = None
    try:
        jti = get_raw_jwt()['jti']
        revoked_jti = UserDBService.revoke_token(jti)
        response = jsonify(revoked_jti), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error)
    finally:
        return response
    
    
@resources.route('/api/auth/register', methods=['POST'])
@jwt_required
@admin_required
def add_user():
    current_app.logger.debug('In POST /api/auth/register')
    response = None
    try:
        posted_user_data = request.get_json()
        # Validate user posted data
        UserValidationService.validate_post(posted_user_data)
        # Check if new email or initials are already in use
        UserDBService.check_unique_mail_and_initiales(posted_user_data.get('email_u'), posted_user_data.get('initiales_u'))

        roles = posted_user_data['roles']
        del posted_user_data['roles']
        new_user = UserDBService.insert(posted_user_data, roles)
        
        response = jsonify(new_user), 201
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_app.logger.debug('In POST /api/auth/refresh')
    try:
        user_identity = get_jwt_identity()
        new_token = {
            'access_token': create_access_token(identity=user_identity)
        }
        return jsonify(new_token), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error)

 
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    try:
        roles = UserDBService.get_user_role_names_by_user_id_or_email(identity)
        return {'roles': roles}
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        return jsonify(error.args[0]), error.args[1]


@jwt.token_in_blacklist_loader
def is_token_in_blacklist(decrypted_token) -> bool:
    try:
        jti = decrypted_token['jti']
        token = UserDBService.get_revoked_token_by_jti(jti)
        return token.get('jti') is not None
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        return jsonify(error.args[0]), error.args[1]
        

# https://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior/
@jwt.revoked_token_loader
def revoked_token_handler():
    try: 
        msg = "Le token n'est plus valide"
        ManageErrorUtils.exception(CodeError.TOKEN_REVOKED_ERROR, TError.TOKEN_ERROR, msg, 401)
    except (ValueError, Exception) as error:
        current_app.logger.debug(error)
        return jsonify(error.args[0]), error.args[1]
   
   
@jwt.expired_token_loader
def expired_token_handler():
    try: 
        msg = "Le token est expiré"
        ManageErrorUtils.exception(CodeError.TOKEN_EXPIRED, TError.TOKEN_ERROR, msg, 401)
    except (ValueError, Exception, ExpiredSignatureError) as error:
        current_app.logger.debug(error)
        return jsonify(error.args[0]), error.args[1]


@jwt.unauthorized_loader
def unauthorized_access_handler(e):
    try: 
        msg = "Manque d'autorisation. Un valide token est demandé"
        ManageErrorUtils.exception(CodeError.TOKEN_REQUIRED, TError.TOKEN_ERROR, msg, 401)
    except (ValueError, Exception) as error:
        current_app.logger.debug(error)
        return jsonify(error.args[0]), error.args[1]
