import pytest

from timetable.db import TimetableDB


@pytest.fixture()
def timetable_db(db_connection) -> TimetableDB:
    return TimetableDB(db_connection)
