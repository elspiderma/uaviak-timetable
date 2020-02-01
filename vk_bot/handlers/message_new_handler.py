from vk_bot.handlers.base_handler import BaseHandler
from utils import utils


class MessageNewHandler(BaseHandler):
    TYPE_ATTACHMENT = 0
    TYPE_TEXT = 1

    def __init__(self, func, text_message=None, head_message=None, ignore_case=False, content_types=None):
        super().__init__(func)

        self.text_message = utils.to_list(text_message)
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

    def _check_message_text(self, message_text: str):
        return len(self.text_message) == 0 or self.text_message.count(message_text) > 0

    def _check_content_types(self, content_types):
        return len(self.content_types) == 0 or self.content_types.count(content_types) > 0

    def _check_message_head(self, message_text: str):
        if len(self.head_message) == 0:
            return True

        if self.ignore_case:
            message_text = message_text.lower()

        for i in self.head_message:
            if self.ignore_case:
                i = i.lower()

            if message_text.startswith(i):
                return True

        return False

    def check(self, obj):
        type_message = self._get_content_types(obj['message'])
        text_message = obj['message']['text']

        return \
            self._check_content_types(type_message) and \
            self._check_message_head(text_message) and \
            self._check_message_text(text_message)
