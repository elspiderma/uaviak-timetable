from dataclasses import dataclass

from db.structures import DbObject


@dataclass
class Group(DbObject):
    """Класс, представляющий расписание.

    Args:
        id: ID группы.
        number: Номер группы.
    """

    id: int
    number: str
