from typing import TYPE_CHECKING

from timetable.exceptions import DataNotFoundError
from timetable.timetable_parser import TimetableParser

if TYPE_CHECKING:
    from timetable.db import TimetableDB
    from timetable.structures import TimetableParsed, TimetableDB


class TimetableSync:
    """Класс для сихронизации сайта БД с сайтом колледжа."""
    def __init__(self, timetable_db: 'TimetableDB'):
        self.timetable_db = timetable_db

    async def _update_timetable(self, timetable_from_db: 'TimetableDB', timetable_from_site: 'TimetableParsed'):
        """
        Обновление уже существуещего расписания
        Args:
            timetable_from_db: Расписание из БД, которое необходимо обновить.
            timetable_from_site: Расписание полученное с сайта.
        """
        pass  # TODO

    async def sync(self):
        """Сихронизирует расписание в БД с расписанием на сайте"""
        timetables_from_site = await TimetableParser.load()

        for timetable in timetables_from_site:
            try:
                timetable_from_db = await self.timetable_db.get_timetable_by_day(timetable.date, timetable.departament)[0]
            except DataNotFoundError:
                await self.timetable_db.add_new_timetable_from_site(timetable)
            else:
                await self._update_timetable(timetable_from_db, timetable)
