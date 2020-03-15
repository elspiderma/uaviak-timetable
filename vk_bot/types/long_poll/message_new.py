from vk_bot.types.message.message import Message
from vk_bot.types.long_poll.client_info import ClientInfo
from vk_bot.types.vk_base_object import VKBaseObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class MessageNew(VKBaseObject):
    def __init__(self,
                 message: Message,
                 client_info: ClientInfo,
                 client: 'VKBot' = None):
        self.message = message
        self.client_info = client_info

        self.client = client

    @classmethod
    def de_dict(cls, data: dict, client: 'VKBot' = None):
        if not data:
            return None

        data['message'] = Message.de_dict(data.get('message'), client)
        data['client_info'] = ClientInfo.de_dict(data.get('client_info'), client)

        return cls(**data, client=client)
