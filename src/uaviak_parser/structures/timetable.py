from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from uaviak_parser.structures import Departaments, Lesson
    import datetime


@dataclass
class Timetable:
    """Дата-класс расписания."""
    # Дополнительная информация
    additional_info: Optional[str]
    # Дата
    date: 'datetime.date'
    # Отделение
    departament: 'Departaments'
    # Пары
    lessons: list['Lesson']

    def __repr__(self):
        return f'<Timetable at {self.date.isoformat()} for {self.departament}>'
