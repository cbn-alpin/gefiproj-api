from api import db
from marshmallow import Schema, fields
from shared.entity import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Funder(Base, db.Model):
    __tablename__ = 'financeur'

    id_financeur = Column(Integer, primary_key=True)
    nom_financeur = Column(String(250), unique=True, nullable=True)
    ref_arret_attributif_financeur = Column(String(250), nullable=True)

    def __init__(self, nom_financeur, ref_arret_attributif_financeur, id_financeur=''):
        if id_financeur != '':
            self.id_financeur = id_financeur
        self.nom_financeur = nom_financeur
        self.ref_arret_attributif_financeur = ref_arret_attributif_financeur


class FunderSchema(Schema):
    id_financeur = fields.Integer()
    nom_financeur = fields.Str()
    ref_arret_attributif_financeur = fields.Str(allow_none=True)
