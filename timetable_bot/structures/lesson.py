from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from uaviak_timetable.timetable import Department

if TYPE_CHECKING:
    from datetime import date


@dataclass
class Teacher:
    id: int
    name: str
    full_name: Optional[str]


@dataclass
class Group:
    id: int
    title: str


@dataclass
class Lesson:
    id: int
    department: Department
    date: 'date'
    group: Group
    number: int
    cabinet: str
    teacher: Teacher
    subject: str
    is_splitting: bool
    is_practice: bool
    is_consultations: bool
    is_exam: bool
