from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from .auth_resources import admin_required

from .db_services import UserDBService
from .entities import User
from .validation_service import UserValidationService

resources = Blueprint('users', __name__)


@resources.route('/api/users', methods=['GET'])
@jwt_required
def get_all_users():
    """This function get list of users

    Returns:
        Response: list of users
    """
    current_app.logger.debug('In GET /api/users')
    response = None
    try:
        users = UserDBService.get_all_users()
        response = jsonify(users), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error)
    finally:
        return response


@resources.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id: int):
    """This function get one user by his id referenced

    Args:
        user_id (int): id of user

    Returns:
        Response: description of one user
    """
    current_app.logger.debug('In GET /api/users/<int:user_id>')
    response = None
    try:
        user = UserDBService.get_user_by_id(user_id)
        response = jsonify(user), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_user(user_id: int):
    """This function update a data of user

    Args:
        user_id (int): id of user

    Returns:
        Response: description of one user
    """
    current_app.logger.debug('In PUT /api/users/<int:user_id>')
    response = None
    try:
        data = dict(request.get_json())
        if 'id_u' not in data:
            data['id_u'] = user_id
            
        # Check forms
        UserValidationService.validate_update(data)
        # Check if user exists
        user = UserDBService.get_user_by_id(user_id)
        # Check if new email or initials are already in use
        UserDBService.check_unique_mail_and_initiales(data.get('email_u'), data.get('initiales_u'), user_id)

        old_roles = user['roles']
        new_roles = data['roles']
        del data['roles']
        response = UserDBService.update(data, old_roles, new_roles)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/users/<int:user_id>/change-password', methods=['PUT'])
@jwt_required
@admin_required
def change_password(user_id: int):
    """This function change the user's password

    Args:
        user_id (int): id of user

    Returns:
        Response: description of user
    """
    current_app.logger.debug('In PUT /api/users/<int:user_id>')
    response = None
    try:
        data = dict(request.get_json())
        """
        
        TODO: pourquoi besoin du old password ????
        
        """
        old_password = data.get('password')
        new_password = data.get('new_password')
        # Check form
        UserValidationService.validate_change_pwd(data)
        # Check if user exists
        user = UserDBService.get_user_by_id(user_id)

        response = UserDBService.change_pwd(user_id, new_password, user['email_u'])
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Impossible de changer le mot de passe de cet utilisateur'}), 500
    finally:
        return response
