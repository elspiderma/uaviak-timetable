import datetime

import pytest

from tests.conftest import generate_parser_timetable
import uaviak_parser
from db.timetable import AdderTimetable, AbstractStatusTimetableHandler, TimetableExistError


class StatusHandler(AbstractStatusTimetableHandler):
    def __init__(self):
        self.ok = []

    def add_timetable_error(self, e: Exception) -> None:
        raise e

    def add_timetable_ok(self, timetable: 'uaviak_parser.structures.timetable') -> None:
        self.ok.append(timetable)


class TestAdderTimetable:
    @pytest.mark.asyncio
    async def test_add_timetable_from_structure(self, db_conn):
        sh = StatusHandler()
        at = AdderTimetable(db_conn, sh)
        parser_timetable1 = generate_parser_timetable(datetime.date(2020, 5, 2),
                                                      uaviak_parser.structures.Departaments.FULL_TIME)
        parser_timetable2 = generate_parser_timetable(datetime.date(2020, 5, 2),
                                                      uaviak_parser.structures.Departaments.CORRESPONDENCE)

        await at.add_timetable_from_structure(parser_timetable1)
        await at.add_timetable_from_structure(parser_timetable2)
        with pytest.raises(TimetableExistError):
            await at.add_timetable_from_structure(parser_timetable1)

        assert sh.ok[0] is parser_timetable1
        assert sh.ok[1] is parser_timetable2

    @pytest.mark.asyncio
    async def test_add_timetable_from_text(self, db_conn, test_timetable):
        sh = StatusHandler()
        at = AdderTimetable(db_conn, sh)

        await at.add_timetable_from_text(test_timetable.text)

        assert sh.ok[0] == test_timetable.structure

    @pytest.mark.asyncio
    async def test_add_timetable_from_html(self, db_conn, test_timetable):
        sh = StatusHandler()
        at = AdderTimetable(db_conn, sh)

        await at.add_timetable_from_html(test_timetable.html)

        assert sh.ok[0] == test_timetable.structure
