from flask import Blueprint, current_app, jsonify, request
from shared.auth import AuthError
from shared.entity import Session

from .entities import Description, DescriptionSchema

# Versions infos

resources = Blueprint('descriptions', __name__)


@resources.route('/descriptions', methods=['GET'])
def get_all_description():
    current_app.logger.info('In GET /descriptions')
    # Fetching from the database
    session = Session()
    descriptions_objects = session.query(Description).all()

    # Transforming into JSON-serializable objects
    schema = DescriptionSchema(many=True)
    descriptions = schema.dump(descriptions_objects)

    # Serializing as JSON
    session.close()
    return jsonify(descriptions)


@resources.route('/descriptions/<int:descId>', methods=['GET'])
def get_one_description(descId):
    # Checks
    check_description_exists

    session = Session()
    description_object = session.query(Description).filter_by(id=descId).first()

    # Transforming into JSON-serializable objects
    schema = DescriptionSchema(many=False)
    description = schema.dump(description_object)

    # Serializing as JSON
    session.close()
    return jsonify(description)


@resources.route('/descriptions', methods=['POST'])
# @requires_auth
def add_description():
    # Mount description object
    current_app.logger.debug('In POST /descriptions')
    posted_desc = DescriptionSchema(only=('mnemonic', 'rank', 'raw_text')) \
        .load(request.get_json())
    desc = Description(**posted_desc, created_by="2")

    # Persist description
    session = Session()
    session.add(desc)
    session.commit()

    # Return created description
    new_desc = DescriptionSchema().dump(desc)
    session.close()
    return jsonify(new_desc), 201


@resources.route('/descriptions/<int:descId>', methods=['PUT'])
# @requires_auth
# TODO: make this indenpotent with meta data
def update_description(descId):
    current_app.logger.debug('In PUT /descriptions/<int:descId>')

    # Load data
    data = dict(request.get_json())
    if id not in data:
        data['id'] = descId

    # Checks
    check_description_exists(data['id'])

    # Mount description object
    data = DescriptionSchema(only=('id', 'mnemonic', 'rank', 'raw_text')) \
        .load(data)
    description = Description(**data, created_by="2")

    # Start DB session
    session = Session()
    session.merge(description)
    session.commit()

    # Return updated description
    updated_desc = DescriptionSchema().dump(description)
    session.close()
    return jsonify(updated_desc), 200


@resources.route('/descriptions/<descId>', methods=['DELETE'])
# @requires_role('admin')
def delete_descriptions(descId):
    check_description_exists(descId)

    session = Session()
    description = session.query(Description).filter_by(id=descId).first()
    session.delete(description)
    session.commit()
    session.close()
    return '', 204


def check_description_exists(descId):
    try:
        session = Session()
        existing_desc = session.query(Description).filter_by(id=descId).first()
        session.close()
        if (existing_desc == None):
            raise ValueError('This description does not exist')
    except ValueError:
        resp = jsonify({"error": {
            'code': 'DESCRIPTION_NOT_FOUND',
            'message': f'Description with id {descId} does not exist.'
        }})
        resp.status_code = 404
        return resp


@resources.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
