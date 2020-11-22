import typing
from dataclasses import dataclass

from structures import Group, Teacher, Lesson

if typing.TYPE_CHECKING:
    from datetime import date


@dataclass
class Timetable:
    date: 'date'
    lessons: typing.List[Lesson]


@dataclass
class TimetableForGroup(Timetable):
    group: Group


@dataclass
class TimetableForTeacher(Timetable):
    teacher: Teacher
