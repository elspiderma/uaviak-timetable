import requests

from vk_bot.types.vk_base_object import VKBaseObject
from vk_bot.types.long_poll.group_result_long_poll import GroupResultLongPoll
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class GroupLongPollServer(VKBaseObject):
    def __init__(self,
                 key: str,
                 server: str,
                 ts: int,
                 client: 'VKBot' = None):
        self.key = key
        self.server = server
        self.ts = ts

        self.client = client

    def get_url(self, wait: int = 25):
        return f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={wait}'

    def request(self, wait: int = 25):
        data = requests.get(self.get_url(wait)).json()
        return GroupResultLongPoll.de_dict(data, self.client)
