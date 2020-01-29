from sqlalchemy import Column, Integer, String, Boolean
from . import Base

from uaviak_timetable import Timetable as TimetableUAviaK


class Timetable(Base):
    __tablename__ = 'timetable'

    id = Column(Integer, primary_key=True)
    group = Column(String(255), index=True)
    subject = Column(String(255))
    number = Column(Integer)
    teacher = Column(String(255), index=True)
    cabinet = Column(Integer)
    is_practice = Column(Boolean)
    is_consultations = Column(Boolean)
    is_splitting = Column(Boolean)

    def __repr__(self):
        return f'<{self.group} {self.subject}>'

    @classmethod
    def get_timetable_site(cls):
        table_db = list()
        table = TimetableUAviaK.load()

        for lesson in table:
            table_db.append(cls(
                group=lesson.group,
                subject=lesson.subject,
                number=lesson.number,
                teacher=lesson.teacher,
                cabinet=lesson.cabinet,
                is_practice=lesson.is_practice,
                is_consultations=lesson.is_consultations,
                is_splitting=lesson.is_splitting
            ))

        return table_db