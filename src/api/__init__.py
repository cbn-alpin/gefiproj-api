from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from shared import config

__version__ = '0.1.0'

db = SQLAlchemy()


def create_api():
    '''
    Create API with Flask.
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_engine_uri()
    db.init_app(app)
    return app
