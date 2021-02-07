from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.api import db
from src.shared.entity import Base
from ..users.entities import UserSchema, User


class Project(Base, db.Model):
    __tablename__ = "projet"

    id_p = Column(db.Integer, primary_key=True)
    code_p = Column(db.Integer, unique=True, nullable=False)
    nom_p = Column(db.String(250), unique=True, nullable=False)
    statut_p = Column(db.Boolean(250), default=False)
    id_u = Column(db.Integer, ForeignKey('utilisateur.id_u'))
    responsable = relationship(User)

    def __init__(self, code_p, nom_p, statut_p, id_u, id_p='', responsable=''):
        if id_p != '':
            self.id_p = id_p
        if responsable != '':
            self.responsable = responsable
        self.code_p = code_p
        self.nom_p = nom_p
        self.statut_p = statut_p
        self.id_u = id_u


class ProjectSchema(Schema):
    id_p = fields.Integer()
    code_p = fields.Integer()
    nom_p = fields.Str()
    statut_p = fields.Bool()
    id_u = fields.Integer()
    responsable = fields.Nested(UserSchema(exclude=['password_u']))
