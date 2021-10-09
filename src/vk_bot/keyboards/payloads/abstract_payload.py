import json


class AbstractPayload:
    COMMAND = ''

    def to_dict(self) -> dict:
        return {'command': self.COMMAND}

    @classmethod
    def from_dict(cls, date: dict) -> 'AbstractPayload':
        raise NotImplemented
