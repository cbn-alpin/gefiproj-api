from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.api import db
from src.shared.entity import Base
from ..fundings.entities import FundingSchema


class Receipt(Base, db.Model):
    __tablename__ = 'recette'

    id_r = Column(Integer, primary_key=True)
    id_f = Column(Integer, ForeignKey('financement.id_f'), nullable=False)
    financement = relationship("Funding")
    montant_r = Column(Float, nullable=False)
    annee_r = Column(Integer, nullable=False)

    def __init__(self, id_f, montant_r, annee_r, id_r=''):
        if id_r != '':
            self.id_r = id_r
        self.id_f = id_f
        self.montant_r = montant_r
        self.annee_r = annee_r


class ReceiptSchema(Schema):
    id_r = fields.Integer()
    id_f = fields.Integer()
    financement = fields.Nested(FundingSchema)
    montant_r = fields.Float()
    annee_r = fields.Integer()
    difference = fields.Float(allow_none=True)

class InputOutput(Base, db.Model):
    __tablename__ = 'entree_sortie'

    id_es = Column(Integer, primary_key=True)
    annee_recette_es = Column(Integer, nullable=False)
    annee_affectation_es = Column(Integer, nullable=False)
    montant_es = Column(Float, nullable=False)

    def __init__(self, annee_recette_es, annee_affectation_es, montant_es, id_es=''):
        if id_es != '':
            self.id_es = id_es
        self.annee_recette_es = annee_recette_es
        self.annee_affectation_es = annee_affectation_es
        self.montant_es = montant_es

class InputOutputSchema(Schema):
    id_es = fields.Integer()
    annee_recette_es = fields.Integer()
    annee_affectation_es = fields.Integer()
    montant_es = fields.Float()