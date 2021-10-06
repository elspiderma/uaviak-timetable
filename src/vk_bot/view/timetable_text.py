from typing import TYPE_CHECKING

from db.structures import TimetableForTeacher, TimetableForGroup, TypesLesson

if TYPE_CHECKING:
    from db.structures import FullLesson, TimetableForSomeone, FullLessonForSomeone


class TimetableText:
    def __init__(self, timetable: 'TimetableForSomeone'):
        self.timetable = timetable

    def _generate_title_line(self) -> str:
        return f'{self.timetable.someone.title}:'

    def _generate_lesson_line(self, lesson: 'FullLessonForSomeone'):
        lesson_str = [f'{lesson.number})', lesson.cabinet, 'каб.', lesson.whose, lesson.subject]

        types_str = self._types_to_str(lesson.types)
        if types_str:
            lesson_str.append(types_str)

        return ' '.join(lesson_str)

    def _types_to_str(self, types: list[TypesLesson]):
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
