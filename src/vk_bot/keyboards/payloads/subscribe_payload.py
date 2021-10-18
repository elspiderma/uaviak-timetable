from enum import Enum

from db.structures import WhoseTimetable
from vk_bot.keyboards.payloads import AbstractPayload


class SubscribeAction(Enum):
    UNSUBSCRIBE = 'unsub'
    SUBSCRIBE = 'sub'


class SubscribePayload(AbstractPayload):
    COMMAND = 'subscribe'

    def __init__(self, id_: int, whose: WhoseTimetable, action: SubscribeAction):
        self.id = id_
        self.whose = whose
        self.action = action

    def to_dict(self) -> dict:
        data = super().to_dict()

        return data | {
            'id': self.id,
            'whose': self.whose.value,
            'action': self.action.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SubscribePayload':
        return cls(data['id'], WhoseTimetable(data['whose']), SubscribeAction(data['action']))
