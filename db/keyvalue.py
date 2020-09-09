from sqlalchemy import Column, Boolean, String, Integer, Index, Date

from . import Base


class KeyValue(Base):
    __tablename__ = 'keyvalue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, unique=True)
    value = Column(String(255))
