import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class VKBaseObject:
    @classmethod
    def de_dict(cls, data: dict, client: 'VKBot' = None):
        if not data:
            return None

        return cls(**data, client=client)

    @classmethod
    def de_list(cls, data: list, client: 'VKBot' = None):
        if not data:
            return None

        objs = list()
        for i in data:
            objs.append(cls.de_dict(i, client=client))

        return objs

    def to_dict(self):
        def parse(val):
            if isinstance(val, VKBaseObject):
                return val.to_dict()
            elif isinstance(val, list):
                return [parse(i) for i in val if i is not None]
            elif isinstance(val, dict):
                return {k: parse(i) for k, i in val.items() if i is not None}
            else:
                return val

        data = self.__dict__.copy()
        data.pop('client')

        return parse(data)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()
