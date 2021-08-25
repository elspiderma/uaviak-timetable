from typing import TYPE_CHECKING

from db.structures import DbObject

if TYPE_CHECKING:
    from db import Database


class Group(DbObject):
    """Класс, представляющий расписание.
    """
    def __init__(self,
                 id: int,
                 number: str,
                 db: 'Database'):
        """
        Args:
            id: ID расписания.
            number: Номер группы.
            db: Подключение к БД.
        """
        super().__init__(db)

        self.id = id
        self.number = number
