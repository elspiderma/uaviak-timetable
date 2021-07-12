from enum import Enum


class TypesLesson(Enum):
    """Возможные типы уроков.
    """
    # Дробление
    SPLIT = 1
    # Практика
    PRACTICAL = 2
    # Консультация
    CONSULTATION = 3
    # Экзамен
    EXAM = 4
