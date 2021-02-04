from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, Float
from src.api import db
from src.shared.entity import Base

class ReceiptAccounting(Base, db.Model):
    __tablename__ = 'recette_comptable'

    id_rc = Column(Integer, primary_key=True)
    montant_rc = Column(Float, nullable=False)
    annee_rc = Column(Integer, nullable=False, unique=True)

    def __init__(self, montant_rc, annee_rc, id_rc=''):
        if id_rc != '':
            self.id_rc = id_rc
        self.montant_rc = montant_rc
        self.annee_rc = annee_rc


class ReceiptAccountingSchema(Schema):
    id_rc = fields.Integer()
    montant_rc = fields.Float()
    annee_rc = fields.Integer()
