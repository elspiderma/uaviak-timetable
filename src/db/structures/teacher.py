from typing import TYPE_CHECKING

from db.structures import DbObject

if TYPE_CHECKING:
    from db import Database


class Teacher(DbObject):
    """Класс, представляющий расписание.
    """
    def __init__(self,
                 id: int,
                 short_name: str,
                 full_name: str,
                 db: 'Database'):
        """
        Args:
            id: ID группы.
            short_name: Имя преподавателя.
            full_name: Полное имя преподавателя.
            db: Подключение к БД.
        """
        super().__init__(db)

        self.id = id
        self.short_name = short_name
        self.full_name = full_name
        self.db = db
