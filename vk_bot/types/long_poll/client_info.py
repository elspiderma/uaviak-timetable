from vk_bot.types.vk_base_object import VKBaseObject
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class ClientInfo(VKBaseObject):
    def __init__(self,
                 button_actions: List[str],
                 lang_id: int,
                 client: 'VKBot'):
        self.button_actions = button_actions
        self.lang_id = lang_id

        self.client = client
