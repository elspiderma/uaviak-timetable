from typing import TYPE_CHECKING

from view.timetable_view.timetable import TimetableViewABC

if TYPE_CHECKING:
    from structures import Lesson, TimetableForTeacher


class TimetableTeacherView(TimetableViewABC):
    @classmethod
    def _get_line_lesson(cls, lesson: 'Lesson'):
        return f'{lesson.number}) {lesson.cabinet} каб. {lesson.group.title} {lesson.subject}'

    @classmethod
    def _get_title_timetable(cls, timetable: 'TimetableForTeacher'):
        return timetable.teacher.name
