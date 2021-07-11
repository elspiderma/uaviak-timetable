from dataclasses import dataclass
from typing import Optional

from uaviak_parser.structures import TypesLesson


@dataclass
class Lesson:
    """Дата-класс пары."""
    # Номер пары
    number: int
    # Предмет
    subject: str
    # Кабинет, где проводится пара
    cabinet: Optional[str]
    # Тип пары
    types: set[TypesLesson]
    # Группа
    group: str
    # Преподаватель
    teacher: str

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return self.number == other.number and \
                   self.subject == other.subject and \
                   self.cabinet == other.cabinet and \
                   self.types == other.types and \
                   self.group == other.group and \
                   self.teacher == other.teacher
        else:
            raise ValueError()
