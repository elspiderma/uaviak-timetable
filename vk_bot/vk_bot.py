import requests
import random
from threading import Thread
from typing import Callable, List, Union

from utils import bool2int

from vk_bot import MessageNewHandler, GroupLongPollServer, VKBaseError, Keyboard


class VKBot:
    def __init__(self,
                 token: str,
                 threaded: bool = True,
                 version_api: str = '5.103',
                 base_url: str = 'https://api.vk.com/method/'):
        self.token = token
        self.version_api = version_api
        self.base_url = base_url
        self.threaded = threaded

        self._message_new_handlers = []

    def _method(self,
                method: str,
                **params):
        params['access_token'] = self.token
        params['v'] = self.version_api

        response = requests.post(
            url=f'{self.base_url}{method}',
            data=params
        )

        data = response.json()

        if 'error' in data:
            raise VKBaseError.de_json(data['error'])

        return data['response']

    def groups_get_long_poll_server(self, group_id: int) -> GroupLongPollServer:
        return GroupLongPollServer.de_dict(self._method(
            'groups.getLongPollServer',
            group_id=group_id
        ), self)

    def messages_send(self, message: str = None, user_id: int = None, random_id: int = None, peer_id: int = None,
                      domain: str = None, chat_id: int = None, user_ids: str = None, lat: Union[int, float] = None,
                      long: Union[int, float] = None, attachment: str = None, reply_to: int = None,
                      forward_messages: str = None, sticker_id: int = None, group_id: int = None,
                      keyboard: Keyboard = None, payload: str = None, dont_parse_links: bool = None,
                      disable_mentions: bool = None, intent: str = None) -> int:
        if random_id is None:
            random_id = random.getrandbits(31) * random.choice([-1, 1])

        return self._method(
            'messages.send',
            peer_id=peer_id,
            user_id=user_id,
            random_id=random_id,
            domain=domain,
            chat_id=chat_id,
            user_ids=user_ids,
            lat=lat,
            long=long,
            message=message,
            attachment=attachment,
            reply_to=reply_to,
            forward_messages=forward_messages,
            sticker_id=sticker_id,
            group_id=group_id,
            keyboard=keyboard.to_json() if keyboard is not None else None,
            payload=payload,
            dont_parse_links=bool2int(dont_parse_links),
            disable_mentions=bool2int(disable_mentions),
            intent=intent
        )

    def messages_edit(self, peer_id: int, message: str = None, message_id: int = None, lat: Union[int, float] = None,
                      long: Union[int, float] = None, attachment: str = None, keep_forward_messages: bool = None,
                      keep_snippets: bool = None, group_id: int = None, dont_parse_links: bool = None) -> int:
        return self._method(
            'messages.edit',
            peer_id=peer_id,
            message=message,
            message_id=message_id,
            lat=lat,
            long=long,
            attachment=attachment,
            keep_forward_messages=bool2int(keep_forward_messages),
            keep_snippets=bool2int(keep_snippets),
            group_id=group_id,
            dont_parse_links=bool2int(dont_parse_links)
        )

    def message_new_handler_add(self, func: Callable,
                                text_message: Union[List[str], str] = None,
                                head_message: Union[List[str], str] = None,
                                ignore_case: bool = False,
                                content_types: Union[List[str], str] = None):
        handler = MessageNewHandler(func, text_message, head_message, ignore_case, content_types)
        self._message_new_handlers.append(handler)

    def process_new_update(self, type_update: str, update: dict):
        if type_update == 'message_new':
            for i in self._message_new_handlers:
                if i.check(update):
                    if self.threaded:
                        task_thread = Thread(target=i.exec, args=(update, ))
                        task_thread.start()
                    else:
                        i.exec(update)
                    break

    def polling(self, group_id: Union[str, int], wait: int = 30):
        long_poll = self.groups_get_long_poll_server(group_id)

        while True:
            result = long_poll.request(wait)

            if result.is_error():
                if result.failed == 1:
                    long_poll.ts = result.ts
                else:
                    long_poll = self.groups_get_long_poll_server(group_id)
                continue

            if result.updates is not None:
                long_poll.ts = result.ts
                for upd in result.updates:
                    self.process_new_update(upd.type, upd.object)
