from marshmallow import Schema, fields
from sqlalchemy import Column

from src.api import db
from src.shared.entity import Base


class Expense(Base, db.Model):
    __tablename__ = "depense"

    id_d = Column(db.Integer, primary_key=True)
    annee_d = Column(db.Integer, nullable=False, unique=True)
    montant_d = Column(db.Float, nullable=False)

    def __init__(self, annee_d: int, montant_d: float, id_d=''):
        if id_d != '':
            self.id_d = id_d
        self.annee_d = annee_d
        self.montant_d = montant_d


class ExpenseSchema(Schema):
    id_d = fields.Integer()
    annee_d = fields.Integer()
    montant_d = fields.Float()
