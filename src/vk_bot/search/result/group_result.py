from typing import TYPE_CHECKING

from vk_bot.search.result.interface_result import InterfaceResult

if TYPE_CHECKING:
    from db.structures import Group, TimetableForGroup
    from datetime import date


class GroupResult(InterfaceResult):
    """Найденая группа.
    """
    def __init__(self, group: 'Group'):
        super().__init__()

        self.group = group

    async def get_dates_timetable(self, count: int = 6) -> list['date']:
        """Получает даты, для которых доступно расписание этой группы.

        Args:
            count: Количество дат.

        Returns:
            Список дат, отсортированных от новых к старым.
        """
        return await self.db.get_date_timetables_with_lesson_for_group(self.group, sort_by_date=True, count=count)

    async def get_timetable(self, date_timetable: 'date') -> 'TimetableForGroup':
        """Получает расписание этогой группы для даты date_timetable.

        Args:
            date_timetable: Дата расписание.

        Returns:
            Расписание или None, если оно не найдено.
        """
        return await self.db.get_full_information_timetable_by_date_for_group(date_timetable, self.group)
