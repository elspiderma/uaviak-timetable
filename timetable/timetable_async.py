import aiohttp
from uaviak_timetable.timetable import Timetable

from utils.hashfile import HashFile
import typing


class TimetableAsync(Timetable):
    @classmethod
    async def _get_html(cls) -> str:
        async with aiohttp.ClientSession() as aiohttp_session:
            response = await aiohttp_session.get(cls.URL_TIMETABLE)
            html = await response.text()

            return html

    @classmethod
    async def load(cls) -> 'TimetableAsync':
        return cls._parse_html_timetable(await cls._get_html())


class TimetableCache(TimetableAsync):
    @classmethod
    async def load(cls) -> typing.Optional[TimetableAsync]:
        html = await cls._get_html()
        hash = HashFile('hashlasttimetable')

        if not hash.is_change(html):
            return None

        hash.edit(html)
        return cls._parse_html_timetable(html)
