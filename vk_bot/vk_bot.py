import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_bot.handlers.message_new_handler import MessageNewHandler


class VKBot:
    def __init__(self, token, version_api='5.103'):
        self.vk = vk_api.VkApi(token=token, api_version=version_api)
        self.vk_api = self.vk.get_api()

        self.message_new_handlers = []

    def message_new_handler_add(self, func, head_message=None, ignore_case=False, content_types: list = None):
        handler = MessageNewHandler(func, head_message, ignore_case, content_types)
        self.message_new_handlers.append(handler)

    def process_new_update(self, type_update, update):
        if type_update in ('message_new', VkBotEventType.MESSAGE_NEW):
            for i in self.message_new_handlers:
                if i.check(update):
                    i.exec(update)
                    break

    def polling(self, group_id, wait=30):
        vk_long_poll = VkBotLongPoll(vk=self.vk, group_id=group_id, wait=wait)
        for event in vk_long_poll.listen():
            self.process_new_update(event.type, event.obj)
