from src.api import db
from marshmallow import Schema, fields
from src.shared.entity import Base
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..receipts.entities import Receipt, ReceiptSchema

class Amount(Base, db.Model):
    __tablename__ = 'montant_affecte'

    id_ma = Column(Integer, primary_key=True)
    montant_ma = Column(Float, nullable=False)
    annee_ma = Column(Integer, nullable=False)
    id_r = Column(Integer, nullable=False)
    #id_r = Column(Integer, ForeignKey('recette.id_r'), nullable=False)
    #recette = relationship("Receipt")

    def __init__(self, id_r, montant_ma, annee_ma, id_ma=''):
        if id_ma != '':
            self.id_ma = id_ma
        self.id_r = id_r
        self.montant_ma = montant_ma
        self.annee_ma = annee_ma


class AmountSchema(Schema):
    id_ma = fields.Integer()
    montant_ma = fields.Float()
    annee_ma = fields.Integer()
    id_r = fields.Integer()
    #recette = fields.Nested(ReceiptSchema)
