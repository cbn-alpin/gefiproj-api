from api import db
from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256 as sha256
from shared.entity import Base
from sqlalchemy import Column


class User(Base, db.Model):
    __tablename__ = "utilisateur"

    id_u = Column(db.Integer, primary_key=True)
    nom_u = Column(db.String(120), unique=False, nullable=False)
    prenom_u = Column(db.String(120), unique=False, nullable=False)
    initiales_u = Column(db.String(120), unique=False, nullable=False)
    email_u = Column(db.String(120), unique=True, nullable=False)
    password_u = Column(db.String(120), nullable=False)

    def __init__(self, nom_u, prenom_u, email_u, initiales_u, password_u, id_u=''):
        if id_u != '':
            self.id_u = id_u
        self.nom_u = nom_u
        self.prenom_u = prenom_u
        self.initiales_u = initiales_u
        self.email_u = email_u
        self.password_u = self.generate_hash(password_u)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)


class UserSchema(Schema):
    id_u = fields.Integer()
    nom_u = fields.Str()
    prenom_u = fields.Str()
    email_u = fields.Str()
    initiales_u = fields.Str()
    password_u = fields.Str()
