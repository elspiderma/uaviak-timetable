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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.additional_info != other.additional_info or \
                    self.date != other.date or \
                    self.departament is not other.departament:
                return False

            lessons_other = other.lessons.copy()
            for i in self.lessons:
                try:
                    lessons_other.remove(i)
                except ValueError:
                    return False

            return len(lessons_other) == 0
        else:
            raise TypeError()
