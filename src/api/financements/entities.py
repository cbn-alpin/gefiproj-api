from datetime import datetime

from api import db
from marshmallow import Schema, fields
from shared.entity import Base
from sqlalchemy import Column, String, Integer, Text, Float, Date
from sqlalchemy.sql import func


class Financement(Base, db.Model):
    __tablename__ = 'financement'
    # __table_args__ = {'schema': 'financement'}

    id_f = Column(Integer, primary_key=True)
    id_p = Column(Integer, nullable=False)
    id_financeur = Column(Integer, nullable=False)
    montant_arrete_f = Column(Float, nullable=False)
    date_arrete_f = Column(Date)
    date_limite_solde_f = Column(Date)
    statut_f = Column(String(250), nullable=False)
    date_solde_f = Column(Date, nullable=False)
    commentaire_admin_f = Column(String(250))
    commentaire_resp_f = Column(String(250))
    numero_titre_f = Column(String(250))
    annee_titre_f = Column(String(250))
    imputation_f = Column(String(250))

    def __init__(self, id_p, id_financeur, montant_arrete_f, statut_f, date_solde_f, date_arrete_f = None, date_limite_solde_f = None, commentaire_admin_f = None, commentaire_resp_f = None, numero_titre_f = None, annee_titre_f = None, imputation_f = None, id_f=''):
        if id_f != '':
            self.id_f = id_f
        self.id_p = id_p
        self.id_financeur = id_financeur
        self.montant_arrete_f = montant_arrete_f
        self.statut_f = statut_f
        self.date_solde_f = date_solde_f
        self.date_arrete_f = date_arrete_f
        self.date_limite_solde_f = date_limite_solde_f
        self.commentaire_admin_f = commentaire_admin_f
        self.commentaire_resp_f = commentaire_resp_f
        self.numero_titre_f = numero_titre_f
        self.annee_titre_f = annee_titre_f
        self.imputation_f = imputation_f

class FinancementSchema(Schema):
    id_f = fields.Integer()
    id_p = fields.Integer()
    id_financeur = fields.Integer()
    montant_arrete_f = fields.Float()
    date_arrete_f = fields.Date()
    date_limite_solde_f = fields.Date()
    statut_f = fields.Str()
    date_solde_f = fields.Date()
    commentaire_admin_f = fields.Str()
    commentaire_resp_f = fields.Str()
    numero_titre_f = fields.Str()
    annee_titre_f = fields.Str()
    imputation_f = fields.Str()