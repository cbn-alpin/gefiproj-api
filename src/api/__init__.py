from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from src.shared import config

__version__ = '0.1.0'

db = SQLAlchemy()
jwt = JWTManager()


def create_api(env='dev'):
    """
    Create API with Flask.
    """
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_engine_uri(env)
    app.config['JWT_SECRET_KEY'] = config.get_jwt_secret()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.get_jwt_expirationt()
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    jwt.init_app(app)
    db.init_app(app)
    return app
