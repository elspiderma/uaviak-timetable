from vk_bot.types.long_poll.update_long_poll import GroupUpdateLongPoll
from vk_bot.handlers.base_handler import BaseHandler
import utils


class MessageNewHandler(BaseHandler):
    TYPE_ATTACHMENT = 0
    TYPE_TEXT = 1

    def __init__(self, func, text_message=None, head_message=None, ignore_case=False, content_types=None):
        super().__init__(func)

        self._ignore_case = ignore_case

        self._text_message = utils.to_list(text_message)
        self._head_message = utils.to_list(head_message)
        self._content_types = utils.to_list(content_types)

    def check(self, obj):
        type_message = self._get_content_types(obj.object.message)
        text_message = obj.object.message.text

        return \
            self._check_content_types(type_message) and \
            self._check_message_head(text_message) and \
            self._check_message_text(text_message)

    @classmethod
    def _get_content_types(cls, message):
        attachments = message.attachments
        geo = message.geo

        if len(attachments) > 0 or geo is not None:
            return cls.TYPE_ATTACHMENT
        else:
            return cls.TYPE_TEXT

    def _check_content_types(self, content_types):
        return len(self._content_types) == 0 or self._content_types.count(content_types) > 0

    def _check_message_head(self, message_text: str):
        if len(self._head_message) == 0:
            return True

        if self._ignore_case:
            message_text = message_text.lower()

        for i in self._head_message:
            if self._ignore_case:
                i = i.lower()

            if message_text.startswith(i):
                return True

        return False

    def _check_message_text(self, message_text: str):
        if self._ignore_case:
            message_text = message_text.lower()
            check_list = utils.string_list_lower(self._text_message)
        else:
            check_list = self._text_message

        return len(check_list) == 0 or check_list.count(message_text) > 0
