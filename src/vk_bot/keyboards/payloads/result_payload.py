from db.structures import WhoseTimetable
from vk_bot.keyboards.payloads import AbstractPayload


class ResultPayload(AbstractPayload):
    COMMAND = 'result'

    def __init__(self, id_: int, whose_timetable: WhoseTimetable):
        self.id = id_
        self.whose_timetable = whose_timetable

    def to_dict(self) -> dict:
        data = super().to_dict()

        return data | {
            'id': self.id,
            'whose_timetable': self.whose_timetable.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ResultPayload':
        return cls(data['id'], WhoseTimetable(data['whose_timetable']))
