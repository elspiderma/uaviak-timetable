from typing import TYPE_CHECKING

import aiohttp
from tortoise.functions import Max
from uaviak_timetable.timetable import Timetable

import db

if TYPE_CHECKING:
    from datetime import date


class TimetableAsync(Timetable):
    """Ассинхронное получение расписания."""
    @classmethod
    async def _get_html(cls) -> str:
        """Ассинхронно получает html страницы."""
        async with aiohttp.ClientSession() as aiohttp_session:
            response = await aiohttp_session.get(cls.URL_TIMETABLE)
            html = await response.text()

            return html

    @classmethod
    async def load(cls) -> 'TimetableAsync':
        return cls._parse_html_timetable(await cls._get_html())


async def get_last_date_timetable() -> 'date':
    """ Получает дату последнего расписания. """
    last_date = await db.Lesson.annotate(last_date=Max('date')).values_list('last_date', flat=True)
    return last_date[0]


def is_group(s: str) -> bool:
    """Проверяет, является ли строка номером группы.

    @param s: Строка для проверки.
    @return: True - если номер группы, иначе False.
    """
    # Номера групп всегда начинаются на цифры.
    # Например 19ис-1, 18ом-1.
    return s[0].isnumeric()

