from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, ForeignKey

from src.api import db
from src.api.role_acces.entities import RoleAccess
from src.api.users.entities import User
from src.shared.entity import Base


class UserRole(Base, db.Model):
    __tablename__ = 'role_utilisateur'

    id_ra = Column(Integer, ForeignKey(RoleAccess.id_ra), primary_key=True)
    id_u = Column(Integer, ForeignKey(User.id_u), primary_key=True)

    def __init__(self, id_ra='', id_u=''):
        if id_ra != '':
            self.id_ra = id_ra
        if id_u != '':
            self.id_u = id_u


class UserRoleSchema(Schema):
    id_ra = fields.Integer()
    id_u = fields.Integer()
