from typing import TYPE_CHECKING

from db import Database

if TYPE_CHECKING:
    from datetime import date


class InterfaceResult:
    def __init__(self):
        self.db = Database.from_keeper()

    async def get_dates_timetable(self, count: int = 6):
        pass

    async def get_timetable(self, date_timetable: 'date' = None):
        raise NotImplemented
