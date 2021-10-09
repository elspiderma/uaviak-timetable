import datetime

from db.structures import WhoseTimetable
from vk_bot.keyboards.payloads import AbstractPayload


class TimetableDatePayload(AbstractPayload):
    COMMAND = 'timetable_date'

    def __init__(self, date: datetime.date, id_: int, whose_timetable: WhoseTimetable):
        self.date = date
        self.id = id_
        self.whose_timetable = whose_timetable

    def to_dict(self) -> dict:
        data = super().to_dict()

        return data | {
            'date': self.date.isoformat(),
            'id': self.id,
            'whose_timetable': self.whose_timetable.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TimetableDatePayload':
        return cls(datetime.date.fromisoformat(data['date']), data['id'], WhoseTimetable(data['whose_timetable']))
