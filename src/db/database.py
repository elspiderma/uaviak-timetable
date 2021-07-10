from typing import TYPE_CHECKING, Optional

from db.structures import Timetable

if TYPE_CHECKING:
    import datetime
    import asyncpg
    import uaviak_parser
    from db.structures import Departaments


class Database:
    """Класс для работы с БД."""

    def __init__(self, connection: 'asyncpg.Connection'):
        self.conn = connection

    async def get_timetable(self, date: 'datetime.date', departament: 'Departaments') -> Optional[Timetable]:
        """
        Получает расписание за определенную дату для определенного отделения.
        Args:
            date: Дата.
            departament: Отделение.

        Returns:
            Расписание или None, если расписание не найдено.
        """
        result = await self.conn.fetchrow(
            'SELECT * FROM timetables WHERE date = $1 AND departament = $2',
            date, departament.value
        )

        if not result:
            return None

        return Timetable.from_record(result, db=self)

    async def add_new_timetable(self, timetable: 'uaviak_parser.structures.Timetable') -> None:
        """Добавляет новое расписание.

        Args:
            timetable: Расписание полученное с сайта
        """
        result = await self.conn.fetch(
            'INSERT INTO timetables(additional_info, date, departament) VALUES ($1, $2, $3) RETURNING id',
            timetable.additional_info, timetable.date, timetable.departament.value
        )
        timetable_id = result[0]['id']

        for lesson in timetable.lessons:
            lesson_types = [i.value for i in lesson.types]
            await self.conn.fetch(
                'SELECT * FROM add_lesson'
                '($1,         $2,            $3,             $4,             $5,           $6,           $7)',
                timetable_id, lesson.number, lesson.subject, lesson.cabinet, lesson_types, lesson.group, lesson.teacher
            )
