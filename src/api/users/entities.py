from api import db
from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256 as sha256
from shared.entity import Base
from sqlalchemy import Column


class User(Base, db.Model):
    __tablename__ = "users"

    id = Column(db.Integer, primary_key=True)
    nom = Column(db.String(120), unique=False, nullable=False)
    prenom = Column(db.String(120), unique=False, nullable=False)
    mail = Column(db.String(120), unique=True, nullable=False)
    login = Column(db.String(120), unique=True, nullable=False)
    password = Column(db.String(120), nullable=False)

    def __init__(self, nom, prenom, mail, login, password, id=''):
        if id != '':
            self.id = id
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.login = login
        self.password = self.generate_hash(password)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)


class UserSchema(Schema):
    id = fields.Integer()
    nom = fields.Str()
    prenom = fields.Str()
    mail = fields.Str()
    login = fields.Str()
    password = fields.Str()
