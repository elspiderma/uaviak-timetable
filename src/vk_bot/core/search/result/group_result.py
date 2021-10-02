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
        return await self.db.get_dates_timetable_for_group(self.group, count)

    async def get_timetable(self, date_timetable: 'date' = None) -> 'TimetableForGroup':
        if date_timetable:
            pass
        else:
            return await self.db.get_last_timetable_for_group_with_lesson(self.group)
