from sqlalchemy import Column, Integer, Boolean, String
from . import Base


class VKUser(Base):
    __tablename__ = 'vk_user'

    id_vk = Column(Integer, primary_key=True, autoincrement=False)
    enable_notify = Column(Boolean, default=False)
    group_notify = Column(String(255), default=None)
