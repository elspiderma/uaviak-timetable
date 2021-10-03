from typing import TYPE_CHECKING, Optional

from vk_bot.core.search.result.group_result import InterfaceResult

if TYPE_CHECKING:
    from db.structures import Teacher, TimetableForTeacher
    from datetime import date


class TeacherResult(InterfaceResult):
    """Найденый преподаватель.
    """
    def __init__(self, teacher: 'Teacher'):
        super().__init__()

        self.teacher = teacher

    async def get_dates_timetable(self, count: int = 6) -> list['date']:
        """Получает даты, для которых доступно расписание этого преподавателя.

        Args:
            count: Количество дат.

        Returns:
            Список дат, отсортированных от новых к старым.
        """
        return await self.db.get_date_timetables_with_lesson_for_teacher(self.teacher, sort_by_date=True, count=6)

    async def get_timetable(self, date_timetable: 'date') -> Optional['TimetableForTeacher']:
        """Получает расписание этого преподавателя для даты date_timetable.

        Args:
            date_timetable: Дата расписание.

        Returns:
            Расписание или None, если оно не найдено.
        """
        return await self.db.get_full_information_timetable_by_date_for_teacher(date_timetable, self.teacher)
