import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from db.structures import DbObject, TypesLesson, Teacher, Group

if TYPE_CHECKING:
    from asyncpg import Record


@dataclass
class Lesson(DbObject):
    id: int
    id_timetable: int
    number: int
    subject: str
    cabinet: str
    types: list[TypesLesson]
    id_group: int
    id_teacher: int

    @classmethod
    def from_record(cls, data: Union['Record', dict]) -> 'Lesson':
        data_dict = dict(data)

        data_dict['types'] = [TypesLesson(i) for i in data_dict['types']]

        return cls.from_dict(data_dict)


@dataclass
class FullLesson(Lesson):
    date: datetime.date
    teacher: Teacher
    group: Group

    @classmethod
    def from_record(cls, data: Union['Record', dict]) -> 'FullLesson':
        data_dict = dict(data)

        assert data_dict['id_group'] == data_dict['g_id']
        assert data_dict['id_teacher'] == data_dict['t_id']

        return cls(
            id=data_dict['l_id'],
            id_timetable=data_dict['id_timetable'],
            number=data_dict['l_number'],
            subject=data_dict['subject'],
            cabinet=data_dict['cabinet'],
            types=[TypesLesson(i) for i in data_dict['types']],
            id_group=data_dict['id_group'],
            id_teacher=data_dict['id_teacher'],
            group=Group(
                id=data_dict.pop('g_id'),
                number=data_dict.pop('g_number')
            ),
            teacher=Teacher(
                id=data_dict['t_id'],
                short_name=data_dict['short_name'],
                full_name=data_dict['full_name']
            ),
            date=data_dict['date']
        )


class FullLessonForSomeone(FullLesson):
    @property
    def whose(self):
        raise NotImplemented


class FullLessonForGroup(FullLessonForSomeone):
    @property
    def whose(self):
        return self.teacher.short_name


class FullLessonForTeacher(FullLessonForSomeone):
    @property
    def whose(self):
        return self.group.number
