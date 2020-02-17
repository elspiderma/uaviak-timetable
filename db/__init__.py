from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

import config

Base = declarative_base()

from db.notify import Notify

engine = create_engine(config.DATA_BASE)
Base.metadata.create_all(engine)

smkr = sessionmaker(bind=engine)
session = scoped_session(smkr)
