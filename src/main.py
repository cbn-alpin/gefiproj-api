# Python libraries

from api import create_api, db
from api.descriptions.resources import resources as descriptions_ressources
from api.financements.resources import resources as financements_ressources
from api.projets.resources import resources as projets_ressources
from api.status.resources import resources as status_ressources
from api.users.resources import resources as users_ressources
from flask_cors import CORS
# External libraries
from flask_migrate import Migrate
# This project files
from shared import logging

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

# Register blueprints
api.register_blueprint(descriptions_ressources)
api.register_blueprint(status_ressources)
api.register_blueprint(financements_ressources)
api.register_blueprint(users_ressources)
api.register_blueprint(projets_ressources)
