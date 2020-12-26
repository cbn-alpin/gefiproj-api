from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..funders.entities import Funder, FunderSchema

from src.api import db
from src.shared.entity import Base


class Funding(Base, db.Model):
    __tablename__ = 'financement'

    id_f = Column(Integer, primary_key=True)
    id_p = Column(Integer, nullable=False)
    id_financeur = Column(Integer, ForeignKey('financeur.id_financeur'), nullable=False)
    financeur = relationship("Funder")
    montant_arrete_f = Column(Float, nullable=False)
    statut_f = Column(String(250), nullable=False)
    date_solde_f = Column(Date)
    date_arrete_f = Column(Date)
    date_limite_solde_f = Column(Date)
    commentaire_admin_f = Column(String(250))
    commentaire_resp_f = Column(String(250))
    numero_titre_f = Column(String(250))
    annee_titre_f = Column(String(250))
    imputation_f = Column(String(250))

    def __init__(self, id_p, id_financeur, montant_arrete_f, statut_f, date_solde_f = None, date_arrete_f=None,
                 date_limite_solde_f=None, commentaire_admin_f='', commentaire_resp_f='', numero_titre_f='',
                 annee_titre_f='', imputation_f='', id_f=''):
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


class FundingSchema(Schema):
    id_f = fields.Integer()
    id_p = fields.Integer()
    id_financeur = fields.Integer()
    financeur = fields.Nested(FunderSchema)
    montant_arrete_f = fields.Float()
    statut_f = fields.Str()
    date_solde_f = fields.Date(allow_none=True)
    date_arrete_f = fields.Date(allow_none=True)
    date_limite_solde_f = fields.Date(allow_none=True)
    commentaire_admin_f = fields.Str(allow_none=True)
    commentaire_resp_f = fields.Str(allow_none=True)
    numero_titre_f = fields.Str(allow_none=True)
    annee_titre_f = fields.Str(allow_none=True)
    imputation_f = fields.Str(allow_none=True)
    difference = fields.Float(allow_none=True)