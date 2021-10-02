from typing import TYPE_CHECKING

from vk_bot.core.search.result.interface_result import InterfaceResult

if TYPE_CHECKING:
    from db.structures import Group, TimetableForGroup
    from datetime import date


class GroupResult(InterfaceResult):
    def __init__(self, group: 'Group'):
        super().__init__()

        self.group = group

    async def get_dates_timetable(self, count: int = 6) -> list['date']:
        return await self.db.get_date_timetables_with_lesson_for_group(self.group, sort_by_date=True, count=count)

    async def get_timetable(self, date_timetable: 'date') -> 'TimetableForGroup':
        return await self.db.get_full_information_timetable_by_date_for_group(date_timetable, self.group)
