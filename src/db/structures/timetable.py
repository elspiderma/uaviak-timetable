from typing import TYPE_CHECKING

from db.structures import Departaments, DbObject

if TYPE_CHECKING:
    from db import Database
    import datetime
    from asyncpg import Record


class Timetable(DbObject):
    """
    Класс, представляющий расписание.
    """
    def __init__(self, id: int, additional_info: str, date: 'datetime.date', departament: Departaments, db: 'Database'):
        super().__init__(db)

        self.id = id
        self.additional_info = additional_info
        self.date = date
        self.departament = departament

        self._lessons = None

    @classmethod
    def from_record(cls, record: 'Record') -> 'Timetable':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.

        Returns:
            Десериализируеммый объект.
        """
        value = dict(record)

        value['departament'] = Departaments(value['departament'])

        return cls.from_dict(value)
