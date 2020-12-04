from api import db
from marshmallow import Schema, fields
from shared.entity import Base
from sqlalchemy import Column, String, Integer


class RoleAccess(Base, db.Model):
    __tablename__ = 'role_acces'

    id_ra = Column(Integer, primary_key=True)
    nom_ra = Column(String(250), nullable=False)
    code_ra = Column(Integer, nullable=False)

    def __init__(self, nom_ra, code_ra, id_ra=''):
        if id_ra != '':
            self.id_ra = id_ra
            self.code_ra = code_ra
        self.nom_ra = nom_ra


class RoleAccessSchema(Schema):
    id_ra = fields.Integer()
    nom_ra = fields.Str()
    code_ra = fields.Integer()
