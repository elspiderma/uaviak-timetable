from enum import Enum


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
