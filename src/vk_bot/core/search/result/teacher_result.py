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
        return await self.db.get_dates_timetable_for_teacher(self.teacher, count)

    async def get_timetable(self, date_timetable: 'date' = None) -> 'TimetableForTeacher':
        if date_timetable:
            pass
        else:
            return await self.db.get_last_timetable_for_teacher_with_lesson(self.teacher)
