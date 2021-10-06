from dataclasses import dataclass

from db.structures import DbObject, ObjectWithTitle


@dataclass
class Group(DbObject, ObjectWithTitle):
    """Класс, представляющий расписание.

    Args:
        id: ID группы.
        number: Номер группы.
    """

    id: int
    number: str

    @property
    def title(self) -> str:
        return self.number
