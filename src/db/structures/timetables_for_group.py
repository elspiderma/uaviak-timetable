from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.structures import Timetable, Group, Lesson


@dataclass
class TimetableForGroup:
    timetable: 'Timetable'
    group: 'Group'
    lessons: list['Lesson']
