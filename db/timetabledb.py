from sqlalchemy import Column, Boolean, String, Integer, Index, Date

from . import Base
import typing
if typing.TYPE_CHECKING:
    from uaviak_timetable.lesson import Lesson
    import datetime


class TimetableDB(Base):
    __tablename__ = 'timetable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    group = Column(String(30))
    number = Column(Integer)
    cabinet = Column(String(255))
    teacher = Column(String(255))
    subject = Column(String(255))

    is_splitting = Column(Boolean, default=False)
    is_practice = Column(Boolean, default=False)
    is_consultations = Column(Boolean, default=False)
    is_exam = Column(Boolean, default=False)


Index('index_group', TimetableDB.group, TimetableDB.number, TimetableDB.date)
Index('index_teacher', TimetableDB.teacher, TimetableDB.number, TimetableDB.date)
