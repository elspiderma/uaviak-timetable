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

    @classmethod
    def from_record(cls, data: 'Record', db: 'Database' = None) -> 'Timetable':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.
            db: Клиент базы данных.

        Returns:
            Десериализируеммый объект.
        """
        data_dict = dict(data)

        data_dict['departament'] = Departaments(data_dict['departament'])

        return cls.from_dict(data_dict, db=db)
