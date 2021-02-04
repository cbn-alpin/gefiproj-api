from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity

from src.shared.entity import Session
from .auth_resources import admin_required
from .db_services import UserDBService
from .entities import UserSchema, User
from .validation_service import UserValidationService

resources = Blueprint('users', __name__)


@resources.route('/api/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    try:
        current_app.logger.debug('In GET /api/users')
        users = UserDBService.get_all_users()
        return jsonify(users), 200
    except Exception as error:
        return jsonify(error), 404


@resources.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id):
    current_app.logger.debug('In GET /api/users/<int:user_id>')

    check_user_exists_by_id(user_id)

    session = Session()
    user_object = session.query(User).filter_by(id_u=user_id).first()

    # Transforming into JSON-serializable objects
    schema = UserSchema(exclude=['password_u'])
    user = schema.dump(user_object)

    user['roles'] = UserDBService.get_user_role_names_by_user_id_or_email(user['email_u'])

    # Serializing as JSON
    session.close()
    return jsonify(user)


@resources.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    current_app.logger.debug('In PUT /api/users/<int:user_id>')

    data = dict(request.get_json())
    if id not in data:
        data['id'] = user_id

    claims = get_jwt_claims()
    is_admin = False
    if 'roles' in claims and 'administrateur' in claims['roles']:
        is_admin = True

    validation_errors = UserValidationService.validate_update(data)
    if len(validation_errors) > 0:
        return jsonify({
            'status': 'error',
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    session = None
    updated_user = None

    # Check if user exists
    try:
        session = Session()
        user = session.query(User).get(user_id)
        if user is None:
            return jsonify({'message': 'user not found'}), 404

        print(is_admin)
        print(get_jwt_identity())
        if user.email_u != get_jwt_identity() and not is_admin:
            return jsonify({'message': 'Cannot an other user'}), 403

        # check if new email or initials are already in use
        user_by_email = UserDBService.get_user_by_email(data.get('email_u'))
        user_by_initiales = UserDBService.get_user_by_initiales(data.get('initiales_u'))
        if (user_by_email and (user_by_email['id_u'] != user_id)) \
                or (user_by_initiales and (user_by_initiales['id_u'] != user_id)):
            message = {'status': 'error', 'type': 'conflict'}
            if user_by_email:
                message['code'] = 'EMAIL_ALREADY_IN_USE'
                message['message'] = 'A user with email <{}> is already in use'.format(data.get('email_u'))
                return jsonify(message), 409

            message['code'] = 'INITIALS_ALREADY_IN_USE'
            message['message'] = 'A user with initials <{}> is already in use'.format(data.get('initiales_u'))
            return jsonify(message), 409

        new_roles = data['roles']
        user = UserDBService.merge_user(user, data)
        session.execute("delete from role_utilisateur where id_u = :user_id",
                        {'user_id': user.id_u})
        session.flush()

        for role in new_roles:
            role_id = 2
            if role == 'administrateur':
                role_id = 1
            session.execute("insert into role_utilisateur values (:role_id, :user_id)",
                            {'user_id': user.id_u, 'role_id': role_id})

        session.commit()

        updated_user = UserSchema(exclude=['password_u']) \
            .dump(user)
        updated_user['roles'] = new_roles
    except Exception as e:
        current_app.logger.error(e)
    finally:
        if session:
            session.close()
    return jsonify(updated_user), 200


@resources.route('/api/users/<int:user_id>/change-password', methods=['POST'])
@jwt_required
def change_password(user_id):
    current_app.logger.debug('In PUT /api/users/<int:user_id>')

    claims = get_jwt_claims()
    is_admin = False
    if 'roles' in claims and 'administrateur' in claims['roles']:
        is_admin = True

    data = dict(request.get_json())
    validation_errors = UserValidationService.validate_change_pwd(data, is_admin)
    if len(validation_errors) > 0:
        return jsonify(validation_errors), 422

    old_password = data.get('password')
    new_password = data.get('new_password')

    session = None
    try:
        session = Session()
        user = session.query(User).get(user_id)
        if not user:
            return jsonify({'message': 'user not found'}), 404

        if not is_admin and user.email_u != get_jwt_identity():
            # change another user password attemp
            return jsonify({'message': 'Cannot change others password'}), 403

        if not is_admin and not User.verify_hash(old_password, user.password_u):
            # couldn't authenticate user who is not admin
            return jsonify({'message': 'Wrong password'}), 401

        user.password_u = User.generate_hash(new_password)
        session.commit()

        return jsonify({'message': 'Password changed'}), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({'message': 'Could  not change password'}), 500
    finally:
        if session:
            session.close()


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
