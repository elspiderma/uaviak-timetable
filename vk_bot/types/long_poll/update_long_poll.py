from vk_bot.types.long_poll.message_new import MessageNew
from vk_bot.types.vk_base_object import VKBaseObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class GroupUpdateLongPoll(VKBaseObject):
    def __init__(self,
                 type: str,
                 object: object,
                 group_id: int,
                 event_id: str,
                 client: 'VKBot' = None):
        self.type = type
        self.object = object
        self.group_id = group_id
        self.event_id = event_id

        self.client = client

    @classmethod
    def de_dict(cls, data: dict, client: 'VKBot' = None):
        if not data:
            return None

        # TODO: Parse 'object'
        if data['type'] == 'message_new':
            data['object'] = MessageNew.de_dict(data.get('object'), client)

        return cls(**data, client=client)
