from typing import List, TYPE_CHECKING, Union, Optional

from utils.multiline_text import GroupMultilineText
if TYPE_CHECKING:
    from structures import TimetableForTeacher, TimetableForGroup, Lesson


class TimetableViewABC:
    @classmethod
    def __get_text_type_lesson(cls, lesson: 'Lesson') -> Optional[str]:
        """Возвращает строку с типом урока. Например: дробление, консультация и др.

        @param lesson: Урок, для формируется строка.
        @return: Строка с типом урока.
        """
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
    def _get_line_lesson(cls, lesson: 'Lesson'):
        """Формирует строку урока.

        @param lesson: Урок.
        @return: Строка урока.
        """
        raise NotImplemented

    @classmethod
    def _get_title_timetable(cls, timetable: Union['TimetableForGroup', 'TimetableForTeacher']):
        """Формирует строку с заголовоком расписания.

        @param timetable: Расписание, для которого необходим заголовок.
        @return: Заголовок расписания.
        """
        raise NotImplemented

    @classmethod
    def get_text(cls,
                 timetables: Union[
                     List[Union['TimetableForGroup', 'TimetableForTeacher']],
                     'TimetableForGroup', 'TimetableForTeacher'
                 ]) -> str:
        """Формирует текст расписания.

        @param timetables: Одно и более расписания для которого/которых быть сформирован текст.
        @return: Текст расписания.
        """
        if not isinstance(timetables, list):
            timetables = [timetables]

        text = GroupMultilineText()
        for timetable in timetables:
            text.new_group()
            text.add_line(f'{cls._get_title_timetable(timetable)}:')
            for lesson in timetable.lessons:
                line_lesson = cls._get_line_lesson(lesson)
                line_type_lesson = cls.__get_text_type_lesson(lesson)
                if line_type_lesson:
                    text.add_line(f'{line_lesson} {line_type_lesson}')
                else:
                    text.add_line(line_lesson)

        text.new_group()
        text.add_line(timetables[0].date.strftime('%a %d.%m'))

        return text.get()
