from enum import Enum

import uaviak_parser


class TypesLesson(Enum):
    """Класс, представляющий тип урока в БД.
    """
    # Дробление
    SPLIT = 'split'
    # Практика
    PRACTICAL = 'practical'
    # Консультация
    CONSULTATION = 'consultation'
    # Экзамен
    EXAM = 'exam'

    @classmethod
    def from_parser_type_lesson(cls, type_lesson: 'uaviak_parser.structures.TypesLesson') -> 'TypesLesson':
        """Конвертирует ENUM типа урока из парсера в тип урока из БД.

        Args:
            type_lesson: Тип урока из парсера.

        Returns:
            Тип урока из БД.
        """
        ratio_departament = {
            uaviak_parser.structures.TypesLesson.SPLIT: cls.SPLIT,
            uaviak_parser.structures.TypesLesson.PRACTICAL: cls.PRACTICAL,
            uaviak_parser.structures.TypesLesson.CONSULTATION: cls.CONSULTATION,
            uaviak_parser.structures.TypesLesson.EXAM: cls.EXAM
        }

        return ratio_departament[type_lesson]
