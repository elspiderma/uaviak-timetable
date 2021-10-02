from typing import TYPE_CHECKING

from vk_bot.core.search.result.group_result import InterfaceResult

if TYPE_CHECKING:
    from db.structures import Teacher, TimetableForTeacher
    from datetime import date


class TeacherResult(InterfaceResult):
    def __init__(self, teacher: 'Teacher'):
        super().__init__()

        self.teacher = teacher

    async def get_dates_timetable(self, count: int = 6) -> list['date']:
        return await self.db.get_date_timetables_with_lesson_for_teacher(self.teacher, sort_by_date=True, count=6)

    async def get_timetable(self, date_timetable: 'date') -> 'TimetableForTeacher':
        return await self.db.get_full_information_timetable_by_date_for_teacher(date_timetable, self.teacher)
