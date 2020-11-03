from datetime import datetime

from api import db
from marshmallow import Schema, fields
from shared.entity import Base
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func


class Description(Base, db.Model):
    __tablename__ = 'description'
    # __table_args__ = {'schema': 'descriptions'}

    id = Column(Integer, primary_key=True)
    mnemonic = Column(String(250), nullable=False)
    rank = Column(String(50), nullable=False)
    raw_text = Column(Text, nullable=False)
    order = Column(String(5))
    sciname = Column(String(150))
    relationships = Column(Text)
    zoobank = Column(String(250))
    type_locality = Column(Text)
    material_examined = Column(Text)
    diagnosis = Column(Text)
    description = Column(Text)
    subtaxa = Column(Text)
    bionomics = Column(Text)
    distribution = Column(Text)
    etymology = Column(Text)
    comments = Column(Text)
    meta_user_id = Column(Integer, default=0)
    meta_date = Column(DateTime, server_default=func.now())
    meta_state = Column(String, default='A')

    def __init__(self, mnemonic, rank, raw_text, created_by=0, id=''):
        if id != '':
            self.id = id
        self.mnemonic = mnemonic
        self.rank = rank
        self.raw_text = raw_text
        self.meta_user_id = created_by  # 'Unknown'
        self.meta_date = datetime.now()
        self.meta_state = 'A'  # Added


class DescriptionSchema(Schema):
    id = fields.Integer()
    mnemonic = fields.Str()
    rank = fields.Str()
    raw_text = fields.Str(data_key="rawText")
    order = fields.Str()
    sciname = fields.Str()
    relationships = fields.Str()
    zoobank = fields.Str()
    type_locality = fields.Str(data_key="typeLocality")
    material_examined = fields.Str(data_key="materialExamined")
    diagnosis = fields.Str()
    description = fields.Str()
    subtaxa = fields.Str()
    bionomics = fields.Str()
    distribution = fields.Str()
    etymology = fields.Str()
    comments = fields.Str()
    meta_user_id = fields.Integer(data_key="metaUserId")
    meta_date = fields.Str(data_key="metaDate")
    meta_state = fields.Str(data_key="metaState")
