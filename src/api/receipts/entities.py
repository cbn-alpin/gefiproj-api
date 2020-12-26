from src.api import db
from marshmallow import Schema, fields
from src.shared.entity import Base
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..fundings.entities import Funding, FundingSchema

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
