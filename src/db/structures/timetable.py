from dataclasses import dataclass
from typing import TYPE_CHECKING, Union, Optional

from db.structures import Departaments, DbObject

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
        db: Подключение к БД.
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
