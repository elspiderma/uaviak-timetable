from dataclasses import dataclass
from typing import TYPE_CHECKING, Union, Optional

from db.structures import Departaments, DbObject, Teacher, Group
from db.structures.lesson import FullLesson

if TYPE_CHECKING:
    import datetime
    from asyncpg import Record


@dataclass
class Timetable(DbObject):
    """Класс, представляющий расписание.

    Attributes:
        id: ID расписания.
        additional_info: Дополнительная информация.
        date: Дата расписания.
        departament: Отделение расписания.
    """

    id: int
    additional_info: Optional[str]
    date: 'datetime.date'
    departament: Departaments

    @classmethod
    def from_record(cls, data: Union['Record', dict]) -> 'Timetable':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.

        Returns:
            Десериализируеммый объект.
        """
        data_dict = dict(data)

        data_dict['departament'] = Departaments(data_dict['departament'])

        return cls.from_dict(data_dict)


@dataclass
class TimetableForGroup(Timetable):
    group: Group
    lessons: list[FullLesson]

    @classmethod
    def from_combined_records(cls, data: list[Union['Record', dict]], group: Group) -> Optional['TimetableForGroup']:
        if not data:
            return None

        data = tuple(dict(i) for i in data)

        # Проверяем, что бы все записи принадлженали одному расписанию.
        if len(set(i['tt_id'] for i in data)) != 1:
            raise ValueError()

        return cls(
            id=data[0]['t_id'],
            additional_info=data[0]['additional_info'],
            date=data[0]['date'],
            departament=Departaments(data[0]['departament']),
            group=group,
            lessons=FullLesson.from_records(data)
        )


@dataclass
class TimetableForTeacher(Timetable):
    teacher: Teacher
    lessons: list[FullLesson]

    @classmethod
    def from_combined_records(cls, data: list[Union['Record', dict]], teacher: Teacher) -> Optional['TimetableForTeacher']:
        if not data:
            return None

        data = tuple(dict(i) for i in data)

        if len(set(i['tt_id'] for i in data)) != 1:
            raise ValueError()

        return cls(
            id=data[0]['t_id'],
            additional_info=data[0]['additional_info'],
            date=data[0]['date'],
            departament=Departaments(data[0]['departament']),
            teacher=teacher,
            lessons=FullLesson.from_records(data)
        )
