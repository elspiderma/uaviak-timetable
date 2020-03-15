from vk_bot.types.vk_base_object import VKBaseObject
from vk_bot.types.long_poll.update_long_poll import GroupUpdateLongPoll
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class GroupResultLongPoll(VKBaseObject):
    def __init__(self,
                 ts: int = None,
                 updates: List[GroupUpdateLongPoll] = None,
                 failed: int = None,
                 client: 'VKBot' = None):
        self.ts = ts
        self.updates = updates
        self.failed = failed

        self.client = client

    def is_error(self):
        return self.failed is not None

    @classmethod
    def de_dict(cls, data: dict, client: 'VKBot' = None):
        if not data:
            return None

        data['updates'] = GroupUpdateLongPoll.de_list(data.get('updates'), client)

        return cls(**data, client=client)
