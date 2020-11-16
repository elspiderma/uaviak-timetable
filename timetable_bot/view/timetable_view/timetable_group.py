from typing import TYPE_CHECKING

from view.timetable_view.timetable import TimetableViewABC

if TYPE_CHECKING:
    from structures import Lesson, TimetableForGroup


class TimetableGroupView(TimetableViewABC):
    @classmethod
    def _get_line_lesson(cls, lesson: 'Lesson'):
        return f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher.name} {lesson.subject}'

    @classmethod
    def _get_title_timetable(cls, timetable: 'TimetableForGroup'):
        return timetable.group.title
