from shared import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.get_engine_uri())

Session = sessionmaker(bind=engine)

Base = declarative_base()
