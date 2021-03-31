import aiohttp
from bs4 import BeautifulSoup

from uaviak_timetable.exceptions import GetHtmlError
from uaviak_timetable.structures import TimetableParsed
from uaviak_timetable.utils import is_string_one_unique_char


class TimetableGetter:
    TIMETABLE_URL = 'https://uaviak.ru/pages/raspisanie-/'
    USER_AGENT = 'TimetableParser/1.0'
    # Классы HTML-элементов, содержащие расписание
    CLASS_WITH_TIMETABLE = (
        'scrolling-text pos1',
        'scrolling-text pos2'
    )

    @classmethod
    async def _load_html(cls) -> str:
        """
        Загружает HTML-страницу с расписанием.

        Returns:
            HTML-страница
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

            text = await response.text()
            return text

    @classmethod
    def _parse_html(cls, text_in_format_html: str) -> list[str]:
        """
        Парсит HTML с расписанием.

        Args:
            text_in_format_html: HTML-страница с расписанием.

        Returns:
            Сырой текст расписания, спарсенный с сайта.
        """
        timetables_text = []

        soup = BeautifulSoup(text_in_format_html, 'html.parser')
        for class_html in cls.CLASS_WITH_TIMETABLE:
            timetable_soup = soup.find(class_=class_html)
            timetable_soup.find(class_='title').extract()  # Удаляем заголовок, "Расписание *** отделения"

            timetables_text.append(timetable_soup.get_text())

        return timetables_text

    @classmethod
    def _prepare_timetable_text(cls, timetable_text: str) -> tuple[str, str, list[str]]:
        """
        Обрабатываем текст расписания, дробит его на отдельные пары.

        Args:
            timetable_text: Сырой текст расписания.

        Returns:
            Заголовок расписания, дополнительная информация о расписании, список пар в виде строк.
        """
        # Расписание на сайте находится в таком формате:
        #
        # <Заголовок>
        # <Доп. информация>
        # -------------------------
        # <Расписание для 1 группы>
        # -------------------------
        # <Расписание для 2 группы>
        # -------------------------
        # <Расписание для n группы>

        timetable_lines = timetable_text.strip().splitlines()

        # Получаем заголовок расписания
        title = timetable_lines.pop(0)
        prepare_timetable_lines = []
        additional_info_lines = []

        is_timetable_begin = False
        for line in timetable_lines:
            line = line.strip()
            line = ' '.join(line.split())  # Удаляем повторяющиеся пробелы

            if line != '':  # Игнорируем пустые линии
                # Строка содержащяя только "-" является разделителем
                if is_string_one_unique_char(line, '-'):
                    is_timetable_begin = True
                elif is_timetable_begin:
                    prepare_timetable_lines.append(line)
                else:
                    additional_info_lines.append(line)

        return title, '\n'.join(additional_info_lines), prepare_timetable_lines

    @classmethod
    async def load(cls) -> list[TimetableParsed]:
        html_timetable = await cls._load_html()
        raw_timetables = cls._parse_html(html_timetable)

        timetables = list()
        for i in raw_timetables:
            title, info, lessons = cls._prepare_timetable_text(i)
            timetables.append(TimetableParsed.parse(title, info, lessons))

        return timetables
