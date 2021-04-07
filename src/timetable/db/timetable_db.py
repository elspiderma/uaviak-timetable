from typing import TYPE_CHECKING, Optional

from timetable.exceptions import DataNotFoundError, TimetableExistError
from timetable.structures import TimetableDB as Timetable, Departament

if TYPE_CHECKING:
    import datetime
    import asyncpg
    from timetable.structures import TimetableParsed


class TimetableDB:
    """Класс для работы с расписание в БД. Он реализует методы для получения, обновления и добавления расписания."""

    def __init__(self, connection: 'asyncpg.Connection'):
        self.conn = connection

    async def get_timetable_by_day(
            self,
            date: 'datetime.date',
            departament: Optional[Departament] = None
    ) -> list[Timetable]:
        """
        Получает расписание за определенный день.
        Args:
            date: Дата расписания.
            departament: Отделение.

        Returns:
            Если `departament` не был передан то возвращет список всех расписаний за день для всех отделений, иначе
            если передан, то возвращает одно расписание для этого отделения.

        Raises:
            DataNotFoundError: Расписание не найдено
        """
        if departament is None:
            result = await self.conn.fetch('SELECT * FROM timetables WHERE date = $1', date)
        else:
            result = await self.conn.fetch('SELECT * FROM timetables WHERE date = $1 AND departament = $2',
                                           date, departament.value)

        if len(result) == 0:
            raise DataNotFoundError(f'timetable for {date} not found')

        timetables = []
        for i in result:
            timetables.append(Timetable(
                id=i['id'],
                additional_info=i['additional_info'],
                date=i['date'],
                departament=Departament(i['departament']),
                lessons=[]
            ))
        return timetables

    async def add_new_timetable_from_site(self, timetable: 'TimetableParsed'):
        """
        Добовляет новое расписание.
        Args:
            timetable: Расписание полученное с сайта
        """
        result = await self.conn.fetch(
            'INSERT INTO timetables(additional_info, date, departament) VALUES ($1, $2, $3) RETURNING id',
            timetable.additional_info, timetable.date, timetable.departament.value
        )
        timetable_id = result[0]['id']

        for lesson in timetable.lessons:
            await self.conn.execute(
                'INSERT INTO '
                'lessons(id_timetable, number, subject, cabinet, types, id_group, id_teacher) '
                'VALUES ($1, $2, $3, $4, $5, '
                '(SELECT id FROM groups WHERE groups.number = $6), '
                '(SELECT id FROM teachers WHERE short_name = $7)'
                ')',
                timetable_id,
                lesson.number,
                lesson.subject,
                lesson.cabinet,
                lesson.types,
                lesson.group,
                lesson.teacher
            )
