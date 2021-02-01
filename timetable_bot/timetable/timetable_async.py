import typing

import aiohttp
from uaviak_timetable.timetable import Timetable


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
