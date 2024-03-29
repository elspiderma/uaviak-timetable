import aiohttp
from bs4 import BeautifulSoup

from uaviak_parser.exceptions import GetHtmlError


class HtmlTimetable:
    """Класс, представляющий HTML-документ с расписанием.
    """
    TIMETABLE_URL = 'https://uaviak.ru/pages/raspisanie/'
    USER_AGENT = 'TimetableParser/1.0'

    # Класс HTML-элемента, с расписанием
    CLASS_WITH_TIMETABLE = ('scrolling-text', 'pos0')

    def __init__(self, html: str):
        """
        Args:
            html: HTML-документ с расписанием.
        """
        self.html = html

    def parse_html(self) -> str:
        """
        Достает из html-страницы текст с расписанием.

        Returns:
            Сырой текст расписания.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        timetable_soup = soup.find(class_=self.CLASS_WITH_TIMETABLE)

        timetable_soup.find(class_='title').extract()  # Удаляем заголовок "Расписание"
        return timetable_soup.get_text()

    @classmethod
    async def load(cls) -> 'HtmlTimetable':
        """
        Загружает HTML-страницу с расписанием.

        Returns:
            HTML-страница с расписанием.
        """
        headers = {
            'User-Agent': cls.USER_AGENT
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                response = await session.get(cls.TIMETABLE_URL)

                response.raise_for_status()
            except aiohttp.ClientResponseError as e:
                raise GetHtmlError(e)

            html = await response.text()
            return cls(html)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.html == other
        elif isinstance(other, HtmlTimetable):
            return self.html == other.html
        else:
            raise TypeError()
