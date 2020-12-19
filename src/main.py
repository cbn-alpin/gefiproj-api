# Python libraries
from flask import render_template
from flask_cors import CORS
# External libraries
from flask_migrate import Migrate

from src.api import create_api, db
from src.api.fundings.resources import resources as funding_ressources
from src.api.projects.resources import resources as projects_ressources
from src.api.status.resources import resources as status_ressources
from src.api.users.resources import resources as users_ressources
# This project files
from src.shared import logging

# Import all models for Migrate


# TODO: use flask config.
# config = config.get()

# Initialize logging
logging.setup()

# Creating the Flask application
api = create_api()

# Database migration
migrate = Migrate(api, db)

# TODO: configure allowed url for CORS with config file parameters.
CORS(api)


# Normal routes
@api.route('/api/docs')
def get_swagger_docs():
    return render_template('swaggerui.html')


# Register blueprints
api.register_blueprint(status_ressources)
api.register_blueprint(funding_ressources)
api.register_blueprint(users_ressources)
api.register_blueprint(projects_ressources)
