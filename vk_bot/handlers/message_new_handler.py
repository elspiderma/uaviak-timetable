from vk_bot.handlers.base_handler import BaseHandler
from utils import utils


class MessageNewHandler(BaseHandler):
    TYPE_ATTACHMENT = 0
    TYPE_TEXT = 1

    def __init__(self, func, head_message=None, ignore_case=False, content_types=None):
        super().__init__(func)

        self.head_message = utils.to_list(head_message)
        self.ignore_case = ignore_case
        self.content_types = utils.to_list(content_types)

    @classmethod
    def _get_content_types(cls, message):
        attachments = message.get('attachments', [])
        geo = message.get('geo')

        if len(attachments) > 0 or geo is not None:
            return cls.TYPE_ATTACHMENT
        else:
            return cls.TYPE_TEXT

    def _check_content_types(self, content_types):
        if len(self.content_types) == 0:
            return True

        for i in self.content_types:
            if i == content_types:
                return True

        return False

    def _check_message_head(self, message_text: str):
        if len(self.head_message) == 0:
            return True

        if self.ignore_case:
            message_text = message_text.lower()

        for i in self.head_message:
            if self.ignore_case:
                i.lower()

            if message_text.startswith(i):
                return True

        return False

    def check(self, obj):
        type_message = self._get_content_types(obj['message'])

        return self._check_content_types(type_message) and self._check_message_head(obj['message']['text'])
