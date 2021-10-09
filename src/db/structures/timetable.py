import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Union, Optional

from db.structures import Departaments, DbObject, Teacher, Group, FullLessonForGroup, FullLessonForTeacher

if TYPE_CHECKING:
    from db.structures import ObjectWithTitleAndId, FullLessonForSomeone
    import datetime
    from asyncpg import Record


class WhoseTimetable(enum.Enum):
    FOR_TEACHER = 'teacher'
    FOR_GROUP = 'group'


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
class TimetableForSomeone(Timetable):
    lessons: list['FullLessonForSomeone']

    whose_timetable: Optional[WhoseTimetable] = field(default=None, init=False)

    @property
    def someone(self) -> 'ObjectWithTitleAndId':
        raise NotImplemented


@dataclass
class TimetableForGroup(TimetableForSomeone):
    group: Group

    def __post_init__(self):
        self.whose_timetable = WhoseTimetable.FOR_GROUP

    @property
    def someone(self) -> Group:
        return self.group

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
            lessons=FullLessonForGroup.from_records(data)
        )


@dataclass
class TimetableForTeacher(TimetableForSomeone):
    teacher: Teacher

    def __post_init__(self):
        self.whose_timetable = WhoseTimetable.FOR_TEACHER

    @property
    def someone(self) -> Teacher:
        return self.teacher

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
            lessons=FullLessonForTeacher.from_records(data)
        )
