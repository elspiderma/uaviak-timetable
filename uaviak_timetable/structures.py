from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TypesLesson(Enum):
    """Возможные типы уроков."""
    # Дробление
    split = 1
    # Практика
    practice = 2
    # Консультация
    consultations = 3
    # Экзамен
    exam = 4


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
    # Дата пары
    date: datetime.date
    # Предмет
    subject: str
    # Кабинет, где проводится пара
    cabinet: str
    # Тип, пары
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
        # TODO
        raise NotImplemented


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
    # Отделение
    departament: list[Departament]


@dataclass
class TimetableParsed(_TimetableBase):
    """Дата-класс представляющий расписание на сайте колледжа."""
    # Уроки
    lessons: list[LessonParsed]

    @classmethod
    def parse(cls, title: str, info: str, lessons: list[str]) -> 'TimetableParsed':
        # TODO
        raise NotImplemented


@dataclass
class TimetableDB(_TimetableBase):
    """Дата-класс представляющий расписание в БД."""
    # ID расписания
    id: int
    # Уроки
    lessons: list[LessonDB]
