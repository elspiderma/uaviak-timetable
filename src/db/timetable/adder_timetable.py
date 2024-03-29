from typing import TYPE_CHECKING, Union

import uaviak_parser
from db import Database
from db.timetable import TimetableExistError

if TYPE_CHECKING:
    import asyncpg
    from db.timetable import AbstractStatusTimetableHandler


class AdderTimetable:
    """Класс, добавляющий новое расписание в БД из разных форматов.
    """

    def __init__(
            self,
            db_conn: 'asyncpg.Connection',
            status_handler: 'AbstractStatusTimetableHandler'
    ):
        """
        Args:
            db_conn: Подключение к БД.
            status_handler: Обработчик добавления расписания.
        """
        self.db_conn = db_conn
        self.db = Database(self.db_conn)

        self.status_handler = status_handler

    async def add_timetable_from_structure(self, timetable: 'uaviak_parser.structures.Timetable') -> None:
        """Добавляет новое расписание в БД из структуры.

        Args:
            timetable: Расписание.

        Raises:
            TimetableExistError - такое расписание уже существует в БД.
        """
        is_exist = await self.db.is_exist_timetable(timetable.date)

        if is_exist:
            self.status_handler.add_timetable_error(TimetableExistError(timetable))
        else:
            await self.db.add_new_timetable(timetable)
            self.status_handler.add_timetable_ok(timetable)

    async def add_timetable_from_text(self, text: Union['uaviak_parser.TextTimetable', str]) -> None:
        """Добавляет расписание из текста.

        Args:
            text: Расписание в текстовом виде, либо объект uaviak_parser.TextTimetable.

        Returns:

        """
        if isinstance(text, str):
            text = uaviak_parser.TextTimetable.parse(text)

        try:
            timetable = text.parse_text()
        except uaviak_parser.exceptions.GetTimetableError as e:
            self.status_handler.add_timetable_error(e)
        else:
            await self.add_timetable_from_structure(timetable)

    async def add_timetable_from_html(self, html: Union['uaviak_parser.HtmlTimetable', str]) -> None:
        """Добавляет расписания из html-документа.

        Args:
            html: html-документ.
        """
        if isinstance(html, str):
            html = uaviak_parser.HtmlTimetable(html)

        await self.add_timetable_from_text(html.parse_html())

    async def add_timetable_from_site(self) -> None:
        """Добавляет расписание с сайта.
        """
        try:
            html = await uaviak_parser.HtmlTimetable.load()
        except uaviak_parser.exceptions.GetHtmlError as e:
            self.status_handler.add_timetable_error(e)
        else:
            await self.add_timetable_from_html(html)
