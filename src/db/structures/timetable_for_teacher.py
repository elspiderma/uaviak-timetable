from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.structures import Timetable, Teacher, Lesson


@dataclass
class TimetableForTeacher:
    timetable: 'Timetable'
    teacher: 'Teacher'
    lessons: list['Lesson']
