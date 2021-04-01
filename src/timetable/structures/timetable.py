import datetime
import typing
from dataclasses import dataclass

from timetable.exceptions import ParseTimetableError
from timetable.structures import Departament, LessonParsed

if typing.TYPE_CHECKING:
    from timetable.structures import LessonDB


@dataclass
class _TimetableBase:
    """Базовый дата-класс расписания."""
    # Дополнительная информация
    additional_info: str
    # Дата
    date: datetime.date
    # Отделение
    departament: Departament


@dataclass
class TimetableParsed(_TimetableBase):
    """Дата-класс представляющий расписание на сайте колледжа."""
    # Уроки
    lessons: list[LessonParsed]

    @classmethod
    def parse(cls, title: str, info: str, lessons: list[str]) -> 'TimetableParsed':
        # Заголовок имеет формат "Расписание [на] {дата} {date_of_week} ({department} отделение)".
        # Например:
        # Расписание 23.03.2021 Вторник (Заочное отделение)
        # или
        # Расписание на 23.03.2021 Вторник (Дневное отделение)
        split_title = title.split()
        if len(split_title) < 5:
            raise ParseTimetableError(title, info, lessons)

        date = split_title[1]
        if date == 'на':  # Если заголовок содержит "на", значит дата во 2 индексе
            date = split_title[2]

        try:
            # Парсинг даты
            day, month, year = date.split('.')
            date = datetime.date(day=int(day), month=int(month), year=int(year))
        except ValueError:
            raise ParseTimetableError(title, info, lessons)

        # Парсинг отделения
        if 'Дневное отделение' in title:
            departament = Departament.FULL_TIME
        elif 'Заочное отделение' in title:
            departament = Departament.CORRESPONDENCE
        else:
            raise ParseTimetableError(title, info, lessons)

        # Парсинг пар
        parsed_lesson = list()
        for i in lessons:
            parsed_lesson.append(LessonParsed.parse(i))

        return cls(
            additional_info=info,
            date=date,
            departament=departament,
            lessons=parsed_lesson
        )


@dataclass
class TimetableDB(_TimetableBase):
    """Дата-класс представляющий расписание в БД."""
    # ID расписания
    id: int
    # Уроки
    lessons: list['LessonDB']
