from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import config

Base = declarative_base()

from .timetable import Timetable
from .vk_user import VKUser

engine = create_engine(config.DATA_BASE)
Base.metadata.create_all(engine)

session = Session(bind=engine)
