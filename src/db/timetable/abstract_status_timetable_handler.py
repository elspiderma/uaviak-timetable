from abc import ABC, abstractmethod

import uaviak_parser


class AbstractStatusTimetableHandler(ABC):
    """Обработчик добавления расписания.
    """
    @abstractmethod
    def add_timetable_error(self, e: Exception) -> None:
        """Обработчик ошибки при добавлении расписания.

        Args:
            e: Исключение.
        """
        pass

    @abstractmethod
    def add_timetable_ok(self, timetable: 'uaviak_parser.structures.timetable') -> None:
        """Обработчик успешного добавления расписания.

        Args:
            timetable: Расписание.
        """
        pass
