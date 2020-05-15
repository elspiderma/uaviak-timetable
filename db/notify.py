from sqlalchemy import Column, Boolean, String, Integer

from . import Base


class Notify(Base):
    __tablename__ = 'notify'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_vk = Column(Integer, index=True)
    is_group = Column(Boolean, default=True)
    search_text = Column(String(255))
