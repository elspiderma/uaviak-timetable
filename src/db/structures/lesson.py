from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from db.structures import DbObject, TypesLesson

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
