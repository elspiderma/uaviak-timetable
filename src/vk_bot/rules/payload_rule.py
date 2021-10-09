from typing import TYPE_CHECKING, Type

from vkbottle.dispatch.rules.bot import PayloadContainsRule

if TYPE_CHECKING:
    from vk_bot.keyboards.payloads import AbstractPayload


class PayloadRule(PayloadContainsRule):
    """Правило, отбирающее сообщения по Payload'у.
    """
    def __init__(self, payload: Type['AbstractPayload']):
        super().__init__({'command': payload.COMMAND})
