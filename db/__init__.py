from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import config

Base = declarative_base()

from db.notify import Notify
from db.cache_photo import CachePhoto
from db.timetabledb import TimetableDB
from db.keyvalue import KeyValue

engine = create_engine(config.DATA_BASE)

smkr = sessionmaker(bind=engine)
session = smkr()
