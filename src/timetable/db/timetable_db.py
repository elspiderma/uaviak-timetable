from typing import TYPE_CHECKING, Optional, Union

from timetable.exceptions import DataNotFoundError
from timetable.structures import TimetableDB, Departament

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
    ) -> Union[TimetableDB, list[TimetableDB]]:
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
        # TODO: Реализовть получение ОДНОГО отделения
        result = await self.conn.fetch('SELECT * FROM timetables WHERE date = $1 AND departament = $2',
                                       date, departament.value)
        if len(result) == 0:
            raise DataNotFoundError(f'timetable for {date} not found')
        timetable = result[0]

        return TimetableDB(
            id=timetable['id'],
            additional_info=timetable['additional_info'],
            date=timetable['date'],
            departament=Departament(timetable['departament']),
            lessons=[]
        )

    async def add_new_timetable_from_site(self, timetable: 'TimetableParsed'):
        """
        Добовляет новое расписание.
        Args:
            timetable: Расписание полученное с сайта
        """
        pass  # TODO
