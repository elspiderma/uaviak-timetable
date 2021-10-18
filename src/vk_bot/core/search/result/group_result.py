from typing import TYPE_CHECKING, Optional, Union

from db import Database
from db.structures import WhoseTimetable
from vk_bot.core.search.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from db.structures import Group, TimetableForGroup, Chat
    from datetime import date


class GroupResult(AbstractResult):
    """Найденая группа.
    """
    def __init__(self, group: 'Group'):
        super().__init__()

        self.group = group

    @property
    def id(self) -> int:
        return self.group.id

    @property
    def whose(self) -> 'WhoseTimetable':
        return WhoseTimetable.FOR_GROUP

    @property
    def title(self) -> str:
        """Возвращает заголовок результата.

        Returns:
            Заголовок.
        """
        return self.group.title

    async def get_dates_timetable(self, count: int = 6) -> list['date']:
        """Получает даты, для которых доступно расписание этой группы.

        Args:
            count: Количество дат.

        Returns:
            Список дат, отсортированных от новых к старым.
        """
        return await self.db.get_date_timetables_with_lesson_for_group(self.group, sort_by_date=True, count=count)

    async def get_timetable(self, date_timetable: 'date') -> Optional['TimetableForGroup']:
        """Получает расписание этогой группы для даты date_timetable.

        Args:
            date_timetable: Дата расписание.

        Returns:
            Расписание или None, если оно не найдено.
        """
        return await self.db.get_full_information_timetable_by_date_for_group(date_timetable, self.group)

    async def subscribe_user(self, chat: Union[int, 'Chat']) -> None:
        await self.db.add_subscribe_group_for_user(chat, self.group)

    async def unsubscribe_user(self, chat: Union[int, 'Chat']) -> None:
        await self.db.delete_subscribe_group_for_user(chat, self.group)

    @classmethod
    async def search(cls, query: str) -> list['GroupResult']:
        """Поиск группы.

        Args:
            query: Поисковой запрос.

        Returns:
            Список групп.
        """
        db = Database.from_keeper()
        return [cls(i) for i in await db.search_groups(query)]

    @classmethod
    async def search_by_id(cls, id_: int) -> Optional['GroupResult']:
        """Ищет группу с ID id_.

        Args:
            id_: ID группы.

        Returns:
            Группа с ID id_.
        """
        db = Database.from_keeper()
        return cls(await db.search_group_by_id(id_))
