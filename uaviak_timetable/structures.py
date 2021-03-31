from dataclasses import dataclass
from enum import Enum
import datetime
from typing import Optional

from uaviak_timetable.exceptions import ParseLessonError, ParseTimetableError
from uaviak_timetable.utils import index_upper


class TypesLesson(Enum):
    """Возможные типы уроков."""
    # Дробление
    SPLIT = 1
    # Практика
    PRACTICAL = 2
    # Консультация
    CONSULTATION = 3
    # Экзамен
    EXAM = 4


class Departament(Enum):
    """Отделения"""
    # Очное
    FULL_TIME = 1
    # Заочное
    CORRESPONDENCE = 2


@dataclass
class GroupDB:
    """Дата-класс предствляющий группу в БД."""
    # ID группы
    id: int
    # Номер группы
    number: str


@dataclass
class TeacherDB:
    """Дата-класс предствляющий преподавателя в БД."""
    # ID преподавателя
    id: int
    # Имя преподавателя
    short_name: str
    # Полное имя преподавателя
    full_name: Optional[str]


@dataclass
class _LessonBase:
    """Базовый класс пары."""
    # Номер пары
    number: int
    # Предмет
    subject: str
    # Кабинет, где проводится пара
    cabinet: str
    # Тип пары
    types: list[TypesLesson]


@dataclass
class LessonParsed(_LessonBase):
    """Дата-класс предствляющий пару на сайте колледжа."""
    # Группа
    group: str
    # Преподаватель
    teacher: str

    @classmethod
    def parse(cls, line: str) -> 'LessonParsed':
        """
        Парсит пару из строки в формате
        группа номер [дрб] кабинет фамилия_препод инициалы_препод предмет [тип_пары]

        Args:
            line: строка для парсинга

        Returns:
            Отпарсенный дата-класс расписания.

        Raises:
            ParseLessonError - ошибка парсинга строки
        """
        # Расписание на сайте находится в следующем формате
        # {группа} {номер} [дрб] {кабинет} {фамилия_препод} {инициалы_препод} {предмет} [{тип_пары}]
        # 17адс1 1 дрб 214 Кольцов В.А. Учебная практика Практика
        split_line = line.split()
        types = list()

        if len(split_line) < 5:
            raise ParseLessonError(line)

        group = split_line.pop(0)  # Извлекаем группу
        try:
            number = int(split_line.pop(0))  # Извлекаем номер кабинета
        except ValueError:
            raise ParseLessonError(line)

        if split_line[0] == "дрб":
            types.append(TypesLesson.SPLIT)
            del split_line[0]

        # Максимальная длина группы 5 символов, если больше, то занчит номер кабинета и фамилия преподавателя слились
        # примеры слияния кабинета и фамилии:
        # 18св-1 1 Св.маШабаев А.В. Учебная практика Практика
        # 19ам-2 2 дрб 410*кАпраушев И.А. Информатика
        tmp = split_line.pop(0)
        if len(tmp) <= 5:
            cabinet = tmp
            teacher = split_line.pop(0)
        else:
            index = index_upper(tmp)

            cabinet = tmp[:index]
            teacher = tmp[index:]

        # Добавляем инициалы к фамилии
        teacher += ' ' + split_line.pop(0)

        if split_line[-1] == 'Практика':
            types.append(TypesLesson.PRACTICAL)
            del split_line[-1]
        elif split_line[-1] in ('Консульт', 'Консультация'):
            types.append(TypesLesson.CONSULTATION)
            del split_line[-1]
        elif split_line[-1] == 'Экзамен':
            types.append(TypesLesson.EXAM)
            del split_line[-1]

        # Все что осталось -- это предмет
        subject = ' '.join(split_line)

        return cls(
            number=number,
            subject=subject,
            cabinet=cabinet,
            types=types,
            group=group,
            teacher=teacher
        )


@dataclass
class LessonDB(_LessonBase):
    """Дата-класс предствляющий пару в БД."""
    # ID пары в БД
    id: int
    # Группа
    group: GroupDB
    # Преподаватель
    teacher: TeacherDB


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
    lessons: list[LessonDB]
