# Python libraries

from flask import render_template, jsonify
from flask_cors import CORS
# External libraries
from flask_migrate import Migrate

from src.api import create_api, db
from src.api.amounts.resources import resources as amounts_ressources
from src.api.expenses.resources import resources as expenses_ressources
from src.api.exports.export_resources import resources as fundings_export_ressources
from src.api.exports.receipts_export_resources import resources as receipts_export_ressources
from src.api.funders.resources import resources as funders_ressources
from src.api.fundings.resources import resources as fundings_ressources
from src.api.projects.resources import resources as projects_ressources
from src.api.receipts.accountings.resources import resources as receipts_accountings_ressources
from src.api.receipts.previous.resources import resources as receipts_previous_ressources
from src.api.receipts.resources import resources as receipts_ressources
from src.api.users.auth_resources import resources as auth_resources
from src.api.users.resources import resources as users_ressources
# This project files
from src.shared import logging

# Import all models for Migrate

# Initialize logging
logging.setup()

# Creating the Flask application
api = create_api()

# Database migration
migrate = Migrate(api, db)

# TODO: configure allowed url for CORS with config file parameters.
CORS(api)


# Normal routes
@api.route('/')
def get_swagger_docs():
    return render_template('swaggerui.html')


@api.route('/health', methods=['GET'])
def health():
	# Handle here any business logic for ensuring you're application is healthy (DB connections, etc...)
    return "Healthy: OK"


@api.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'status': 'error',
        'type': 'NOT_FOUND',
        'code': 'RESOURCE_NOT_FOUND',
        'message': 'The requested URL was not found on the server. You can check available endpoints at /'
    }), 404


# Register blueprints
api.register_blueprint(fundings_ressources)
api.register_blueprint(users_ressources)
api.register_blueprint(auth_resources)
api.register_blueprint(projects_ressources)
api.register_blueprint(funders_ressources)
api.register_blueprint(receipts_ressources)
api.register_blueprint(amounts_ressources)
api.register_blueprint(expenses_ressources)
api.register_blueprint(fundings_export_ressources)
api.register_blueprint(receipts_export_ressources)
api.register_blueprint(receipts_accountings_ressources)
api.register_blueprint(receipts_previous_ressources)
