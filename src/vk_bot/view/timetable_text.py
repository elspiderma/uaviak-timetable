from typing import Union, TYPE_CHECKING

from db.structures import TimetableForTeacher, TimetableForGroup, TypesLesson

if TYPE_CHECKING:
    from db.structures import FullLesson, DbObject


def _types_to_str(types: list[TypesLesson]):
    def convert(t: list[TypesLesson]) -> tuple[str]:
        types2string = {
            TypesLesson.EXAM: 'экз',
            TypesLesson.SPLIT: 'дрб',
            TypesLesson.PRACTICAL: 'практ',
            TypesLesson.CONSULTATION: 'конс'
        }

        return tuple(types2string[i] for i in t)

    types_str = convert(types)
    if not types_str:
        return None

    return f"({', '.join(types_str)})"


class _TimetableText:
    def __init__(self, timetable: Union[TimetableForGroup, TimetableForTeacher]):
        self.timetable = timetable

    def _generate_title_line(self) -> str:
        raise NotImplemented

    def _generate_lesson_line_without_type(self, lesson: 'FullLesson') -> list[str]:
        raise NotImplemented

    def _generate_lesson_line(self, lesson: 'FullLesson'):
        lesson_str = self._generate_lesson_line_without_type(lesson)

        types_str = _types_to_str(lesson.types)
        if types_str:
            lesson_str.append(types_str)

        return ' '.join(lesson_str)

    def _generate_date_line(self) -> str:
        return self.timetable.date.strftime('%a %d.%m')

    def generate_text(self) -> str:
        lines = list()

        lines.append(self._generate_title_line())
        for lesson in self.timetable.lessons:
            lines.append(self._generate_lesson_line(lesson))

        lines.append('')
        lines.append(self._generate_date_line())

        return '\n'.join(lines)


class TimetableGroupText(_TimetableText):
    def _generate_title_line(self) -> str:
        return self.timetable.group.number

    def _generate_lesson_line_without_type(self, lesson: 'FullLesson') -> list[str]:
        return [f'{lesson.number})', lesson.cabinet, 'каб.', lesson.teacher.short_name, lesson.subject]


class TimetableTeacherText(_TimetableText):
    def _generate_title_line(self) -> str:
        return self.timetable.teacher.short_name

    def _generate_lesson_line_without_type(self, lesson: 'FullLesson') -> list[str]:
        return [f'{lesson.number})', lesson.cabinet, 'каб.', lesson.group.number, lesson.subject]


def generate_text_timetable(timetable: 'DbObject') -> _TimetableText:
    if isinstance(timetable, TimetableForGroup):
        return TimetableGroupText(timetable)
    elif isinstance(timetable, TimetableForTeacher):
        return TimetableTeacherText(timetable)
    else:
        raise ValueError()
