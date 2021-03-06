from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column

from src.api import db
from src.shared.entity import Base

"""
This class defines the "user" entity and manages the tokens.
"""
class User(Base, db.Model):
    __tablename__ = "utilisateur"
    __table_args__ = {'extend_existing': True}

    id_u = Column(db.Integer, primary_key=True)
    nom_u = Column(db.String(120), nullable=False)
    prenom_u = Column(db.String(120), nullable=False)
    initiales_u = Column(db.String(3), nullable=False)
    email_u = Column(db.String(120), unique=True, nullable=False)
    password_u = Column(db.String(120), nullable=False)
    active_u = Column(db.Boolean(5), default=True)

    def __init__(self, nom_u, prenom_u, email_u, initiales_u, active_u, password_u='', id_u=''):
        if id_u != '':
            self.id_u = id_u
        if password_u != '':
            self.password_u = self.generate_hash(password_u)
        self.nom_u = nom_u
        self.prenom_u = prenom_u
        self.initiales_u = initiales_u
        self.email_u = email_u
        self.active_u = active_u

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(email_u=login).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(Schema):
    id_u = fields.Integer()
    nom_u = fields.Str()
    prenom_u = fields.Str()
    email_u = fields.Str()
    initiales_u = fields.Str()
    active_u = fields.Bool()
    password_u = fields.Str()


class RevokedToken(Base, db.Model):
    __tablename__ = "revoked_tokens"
    id = Column(db.Integer, primary_key=True)
    jti = Column(db.String(120), nullable=False)

    def __init__(self, jti: str, id=''):
        if id != '':
            self.id = id
        self.jti = jti


class RevokedTokenSchema(Schema):
    id = fields.Integer()
    jti = fields.Str()
