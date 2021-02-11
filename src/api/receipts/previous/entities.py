from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, Float

from src.api import db
from src.shared.entity import Base


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
