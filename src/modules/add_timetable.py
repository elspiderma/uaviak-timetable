from updater import AdderTimetable, AbstractStatusTimetableHandler, TimetableExistError
from db import ConnectionKeeper
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Configuration
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


async def add_timetable_from_site(config: 'Configuration') -> None:
    """Добавляет расписание с сайта колледжа.

    Args:
        config: Конфигурация приложения.
    """
    await ConnectionKeeper.init_connection_from_config(config)
    conn_db = ConnectionKeeper.get_connection()

    at = AdderTimetable(conn_db, ConsoleLogStatusHandler())
    await at.add_timetable_from_site()

    await ConnectionKeeper.close_connection()


async def add_timetable_from_html_file(config: 'Configuration', filename: str) -> None:
    """Добавлянет расписание из HTML-файла.

    Args:
        config: Конфигурация приложения.
        filename: Имя файла c HTML-документом.
    """
    await ConnectionKeeper.init_connection_from_config(config)
    conn_db = ConnectionKeeper.get_connection()

    at = AdderTimetable(conn_db, ConsoleLogStatusHandler())
    with open(filename, 'r') as f:
        await at.add_timetable_from_html(f.read())

    await ConnectionKeeper.close_connection()
