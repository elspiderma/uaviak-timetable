from uaviak_timetable import Timetable
from .base import CommandBase
from utils.text_creater import TextCreater

class TimetableCommand(CommandBase):
    @classmethod
    def _gen_timetable_text(cls, tt_group, group):
        text = TextCreater()
        for lesson in tt_group:
            text.add(cls._gen_lesson_text(lesson))

        return str(text)

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
    def _gen_lesson_text(cls, lesson):
        raise NotImplementedError
