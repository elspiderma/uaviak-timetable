import asyncio
from typing import TYPE_CHECKING

from db import ConnectionKeeper
from db.timetable import AdderTimetable, AbstractStatusTimetableHandler, TimetableExistError
from modules import AbstractConfigModule

if TYPE_CHECKING:
    import uaviak_parser


class ConsoleLogStatusHandler(AbstractStatusTimetableHandler):
    """Логирует добавление расписания в консоль.
    """
    def add_timetable_error(self, e: Exception) -> None:
        if isinstance(e, TimetableExistError):
            print(f'Расписание {e.timetable} уже существует.')
        else:
            print(f'Ошибка добавления расписания: {e}')

    def add_timetable_ok(self, timetable: 'uaviak_parser.structures.timetable') -> None:
        print(f'Расписание {timetable} успешно добавлено')


class AddTimetableModule(AbstractConfigModule):
    """Модуль, добавляющий расписание в БД.
    """
    @staticmethod
    async def _add_timetable_from_site() -> None:
        """Добавляет расписание с сайта колледжа.
        """
        conn_db = ConnectionKeeper.get_connection()

        at = AdderTimetable(conn_db, ConsoleLogStatusHandler())
        await at.add_timetable_from_site()

    @staticmethod
    async def _add_timetable_from_html_file(filename: str) -> None:
        """Добавлянет расписание из HTML-файла.

        Args:
            filename: Имя файла c HTML-документом.
        """
        conn_db = ConnectionKeeper.get_connection()

        at = AdderTimetable(conn_db, ConsoleLogStatusHandler())
        with open(filename, 'r') as f:
            await at.add_timetable_from_html(f.read())

    async def _run(self) -> None:
        """Добавляет новое расписание.
        """
        await ConnectionKeeper.init_connection_from_config(self.config)

        if self.args.file:
            await self._add_timetable_from_html_file(self.args.file)
        else:
            await self._add_timetable_from_site()

        await ConnectionKeeper.close_connection()

    def run(self) -> None:
        """Обертка над `self._run` для запуска из sync.
        """
        asyncio.run(self._run())
