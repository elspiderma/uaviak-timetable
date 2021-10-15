from typing import TYPE_CHECKING, Optional

from db import Database
from db.structures import WhoseTimetable
from vk_bot.core.search.result.group_result import AbstractResult

if TYPE_CHECKING:
    from db.structures import Teacher, TimetableForTeacher
    from datetime import date


class TeacherResult(AbstractResult):
    """Найденный преподаватель.
    """
    def __init__(self, teacher: 'Teacher'):
        super().__init__()

        self.teacher = teacher

    @property
    def id(self) -> int:
        return self.teacher.id

    @property
    def whose(self) -> 'WhoseTimetable':
        return WhoseTimetable.FOR_TEACHER

    @property
    def title(self) -> str:
        """Возвращает заголовок результата.

        Returns:
            Заголовок.
        """
        return self.teacher.title

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

    @classmethod
    async def search(cls, query: str) -> list['TeacherResult']:
        """Поиск преподавателя.

        Args:
            query: Поисковой запрос.

        Returns:
            Список подходящих преподавателей.
        """
        db = Database.from_keeper()
        return [cls(i) for i in await db.search_teachers(query)]

    @classmethod
    async def search_by_id(cls, id_: int) -> Optional['TeacherResult']:
        """Ищет преподавателя с ID id_.

        Args:
            id_: ID преподавателя.

        Returns:
            Преподаватель с ID id_.
        """
        db = Database.from_keeper()
        return cls(await db.search_teacher_by_id(id_))
