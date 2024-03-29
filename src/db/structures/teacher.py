from dataclasses import dataclass

from db.structures import DbObject, ObjectWithTitleAndId


@dataclass
class Teacher(DbObject, ObjectWithTitleAndId):
    """Класс, представляющий расписание.

    Args:
        id: ID группы.
        short_name: Имя преподавателя.
        full_name: Полное имя преподавателя.
    """

    id: int
    short_name: str
    full_name: str

    @property
    def title(self) -> str:
        return self.short_name
