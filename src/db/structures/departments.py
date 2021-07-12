from enum import Enum

import uaviak_parser


class Departaments(Enum):
    """Класс, представляющий отделение в БД.
    """
    # Очное
    FILL_TIME = 'full_time'
    # Заочное
    CORRESPONDENCE = 'correspondence'

    @classmethod
    def from_parser_departaments(cls, departaments: 'uaviak_parser.structures.Departaments'):
        """Конвертирует ENUM департамента из парсера в департамент из БД.

        Args:
            departaments: Департамент из парсера.

        Returns:
            Департамент из БД.
        """
        ratio_departament = {
            uaviak_parser.structures.Departaments.FULL_TIME: cls.FILL_TIME,
            uaviak_parser.structures.Departaments.CORRESPONDENCE: cls.CORRESPONDENCE
        }

        return ratio_departament[departaments]
