from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from uaviak_parser.structures import Departaments, Lesson
    import datetime


@dataclass
class Timetable:
    """Дата-класс расписания."""
    # Дата
    date: 'datetime.date'
    # Пары
    lessons: list['Lesson']

    def __repr__(self):
        return f'<Timetable at {self.date.isoformat()}>'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.date != other.date:
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
