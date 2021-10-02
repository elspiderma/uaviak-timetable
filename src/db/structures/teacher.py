from dataclasses import dataclass

from db.structures import DbObject


@dataclass
class Teacher(DbObject):
    """Класс, представляющий расписание.

    Args:
        id: ID группы.
        short_name: Имя преподавателя.
        full_name: Полное имя преподавателя.
    """

    id: int
    short_name: str
    full_name: str
