from typing import TYPE_CHECKING, Union

import uaviak_parser
from db import Database
from db.structures import Departaments, TypesLesson
from updater import TimetableExistError

if TYPE_CHECKING:
    import asyncpg
    from updater import AbstractStatusTimetableHandler


class AdderTimetable:
    """Класс, добавляющий новое расписание в БД из разных форматов.
    """
    def __init__(
            self,
            conn_db: 'asyncpg.Connection',
            status_handler: 'AbstractStatusTimetableHandler'
    ):
        """
        Args:
            conn_db: Подключение к БД.
            status_handler: Обработчик добавления расписания.
        """
        self.conn_db = conn_db
        self.db = Database(self.conn_db)

        self.status_handler = status_handler

    async def add_timetable_from_structure(self, timetable: 'uaviak_parser.structures.Timetable') -> None:
        """Добавляет новое расписание в БД из структуры.

        Args:
            timetable: Расписание.

        Raises:
            TimetableExistError - такое расписание уже существует в БД.
        """
        timetable_db = await self.db.get_timetable(timetable.date,
                                                   Departaments.from_parser_departaments(timetable.departament))

        if timetable_db is not None:
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

        for str_timetable in html.parse_html():
            await self.add_timetable_from_text(str_timetable)

    async def add_timetable_from_site(self) -> None:
        """Добавляет расписание с сайта.
        """
        try:
            html = await uaviak_parser.HtmlTimetable.load()
        except uaviak_parser.exceptions.GetHtmlError as e:
            self.status_handler.add_timetable_error(e)
        else:
            await self.add_timetable_from_html(html)
