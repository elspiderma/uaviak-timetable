from abc import ABC

import uaviak_parser


class AbstractStatusTimetableHandler(ABC):
    """Обработчик статуса добавления расписания.
    """
    def add_timetable_error(self, e: Exception) -> None:
        """Обработчик .

        Args:
            e: Исключение.
        """
        raise NotImplemented

    def add_timetable_ok(self, timetable: 'uaviak_parser.structures.timetable') -> None:
        """Обработчик успешного добавления расписания.

        Args:
            timetable: Расписание.
        """
        raise NotImplemented
