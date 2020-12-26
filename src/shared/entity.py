from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Session = SQLAlchemy().session

Base = declarative_base()
