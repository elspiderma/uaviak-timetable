from abc import ABC

from .base import CommandBase
from utils.text_creater import TextCreater


class TimetableCommand(CommandBase, ABC):
    @classmethod
    def _gen_timetable_text(cls, tt_group):
        text = TextCreater()
        for lesson in tt_group:
            line = cls._gen_lesson_text(lesson)
            text.add(cls._append_type_lesson(lesson, line))

        return text

    @staticmethod
    def _gen_type_lesson(lesson):
        types = list()

        if lesson.is_splitting:
            types.append('дроб.')
        if lesson.is_practice:
            types.append('прак.')
        if lesson.is_consultations:
            types.append('консулт.')

        if len(types) == 0:
            return None

        s = ', '.join(types)
        return f'({s})'

    @classmethod
    def _append_type_lesson(cls, lesson, s):
        type_str = cls._gen_type_lesson(lesson)

        if type_str is not None:
            s += f' {type_str}'

        return s

    @classmethod
    def _gen_lesson_text(cls, lesson):
        raise NotImplementedError

    def _message_starts_with(self, prefix, ignore_case=True):
        text_message = self.event['message']['text']

        if ignore_case:
            text_message = text_message.lower()
            prefix = prefix.lower()

        if text_message.startswith(prefix):
            return True
        else:
            return False
