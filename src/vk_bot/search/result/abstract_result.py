from typing import TYPE_CHECKING, Optional

from db import Database
from db.structures import ObjectWithTitleAndId

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone
    from datetime import date


class AbstractResult(ObjectWithTitleAndId):
    """Интерфейс для результата поиска.
    """
    def __init__(self):
        self.db = Database.from_keeper()

    async def get_dates_timetable(self, count: int) -> list['date']:
        """Получает даты, для которых доступно расписание.

        Args:
            count: Количество дат.

        Returns:
            Список дат, отсортированных от новых к старым.
        """
        pass

    async def get_timetable(self, date_timetable: 'date') -> Optional['TimetableForSomeone']:
        """Получает расписание для даты date_timetable.

        Args:
            date_timetable: Дата расписание.

        Returns:
            Расписание или None, если оно не найдено.
        """
        raise NotImplemented

    @classmethod
    async def search(cls, query: str) -> list['AbstractResult']:
        """Поиск.

        Args:
            query: Поисковой запрос.

        Returns:
            Результаты поиска.
        """
        raise NotImplemented

    @classmethod
    async def search_by_id(cls, id_: int) -> Optional['AbstractResult']:
        """Поиск по ID.

        Args:
            id_: Искомый ID.

        Returns:
            Результат с нужным ID.
        """
        raise NotImplemented
