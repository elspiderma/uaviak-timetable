from sqlalchemy import Column, String, Integer
from . import Base


class CachePhoto(Base):
    __tablename__ = 'cache_photo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, index=True, unique=True)
    id_vk = Column(String)
