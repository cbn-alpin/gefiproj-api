from api import db
from marshmallow import Schema, fields
from shared.entity import Base
from sqlalchemy import Column, String, Integer, Float, Date


class Funding(Base, db.Model):
    __tablename__ = 'financement'

    id_f = Column(Integer, primary_key=True)
    id_p = Column(Integer, nullable=False)
    id_financeur = Column(Integer, nullable=False)
    montant_arrete_f = Column(Float, nullable=False)
    statut_f = Column(String(250), nullable=False)
    date_solde_f = Column(Date, nullable=False)
    date_arrete_f = Column(Date, nullable=True)
    date_limite_solde_f = Column(Date, nullable=True)
    commentaire_admin_f = Column(String(250), nullable=True)
    commentaire_resp_f = Column(String(250), nullable=True)
    numero_titre_f = Column(String(250), nullable=True)
    annee_titre_f = Column(String(250), nullable=True)
    imputation_f = Column(String(250), nullable=True)

    def __init__(self, id_p, id_financeur, montant_arrete_f, statut_f, date_solde_f, date_arrete_f='',
                 date_limite_solde_f='', commentaire_admin_f='', commentaire_resp_f='', numero_titre_f='',
                 annee_titre_f='', imputation_f='', id_f=''):
        if id_f != '':
            self.id_f = id_f

        if date_arrete_f != ('' or None):
            self.date_arrete_f = date_arrete_f

        if date_limite_solde_f != ('' or None):
            self.date_limite_solde_f = date_limite_solde_f

        if commentaire_admin_f != ('' or None):
            self.commentaire_admin_f = commentaire_admin_f

        if commentaire_resp_f != ('' or None):
            self.commentaire_resp_f = commentaire_resp_f

        if numero_titre_f != ('' or None):
            self.numero_titre_f = numero_titre_f

        if annee_titre_f != ('' or None):
            self.annee_titre_f = annee_titre_f

        if imputation_f != ('' or None):
            self.imputation_f = imputation_f

        self.id_p = id_p
        self.id_financeur = id_financeur
        self.montant_arrete_f = montant_arrete_f
        self.statut_f = statut_f
        self.date_solde_f = date_solde_f


class FundingSchema(Schema):
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
