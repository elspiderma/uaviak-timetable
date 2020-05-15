from vkbottle import Message
from vkbottle.rule import AbstractMessageRule

import config


class AdminMessage(AbstractMessageRule):
    async def check(self, message: Message) -> bool:
        return message.peer_id in config.ADMIN_ID
