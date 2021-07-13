import datetime

import pytest

from db import Database
from db.structures import Departaments, TypesLesson


class TestDatabase:
    @pytest.mark.asyncio
    async def test_is_exist_timetable(self, db_conn):
        db = Database(db_conn)
        date = datetime.date(2020, 5, 5)
        departament = Departaments.FILL_TIME
        await db_conn.fetch('INSERT INTO timetables(date, departament) VALUES ($1, $2)',
                            date, departament.value)

        result_yes = await db.is_exist_timetable(date, departament)
        result_no_1 = await db.is_exist_timetable(datetime.date(2021, 8, 6), departament)
        result_no_2 = await db.is_exist_timetable(date, Departaments.CORRESPONDENCE)
        result_no_3 = await db.is_exist_timetable(datetime.date(2021, 8, 6), Departaments.CORRESPONDENCE)

        assert result_yes is True
        assert result_no_1 is False
        assert result_no_2 is False
        assert result_no_3 is False

    @pytest.mark.asyncio
    async def test_get_timetable(self, db_conn):
        db = Database(db_conn)

        additional_info = 'Test info'
        date = datetime.date(2003, 3, 29)
        departament = Departaments.CORRESPONDENCE

        await db_conn.fetch('INSERT INTO timetables(additional_info, date, departament) VALUES ($1, $2, $3)',
                            additional_info, date, departament.value)

        result_exist = await db.get_timetable(date, departament)
        result_no_exist = await db.get_timetable(date, Departaments.FILL_TIME)

        assert result_exist.additional_info == additional_info
        assert result_exist.date == date
        assert result_exist.departament is Departaments.CORRESPONDENCE

        assert result_no_exist is None

    @pytest.mark.asyncio
    async def test_add_timetable(self, db_conn, test_timetable):
        parser_timetable = test_timetable.structure
        db = Database(db_conn)

        await db.add_new_timetable(parser_timetable)

        timetable_record = await db_conn.fetchrow(
            'SELECT * FROM timetables WHERE date = $1 AND departament = $2',
            parser_timetable.date,
            Departaments.from_parser_departaments(parser_timetable.departament).value
        )
        assert timetable_record['additional_info'] == parser_timetable.additional_info
        assert timetable_record['date'] == parser_timetable.date
        assert timetable_record['departament'] == \
               Departaments.from_parser_departaments(parser_timetable.departament).value

        lessons = await db_conn.fetch(
            """SELECT lessons.*, groups.number as gn, teachers.short_name as ts FROM lessons
            INNER JOIN timetables on timetables.id = lessons.id_timetable
            INNER JOIN groups on groups.id = lessons.id_group
            INNER JOIN teachers on teachers.id = lessons.id_teacher
            WHERE timetables.date = $1 AND timetables.departament = $2""",
            parser_timetable.date,
            Departaments.from_parser_departaments(parser_timetable.departament).value
        )

        for db, parser in zip(lessons, parser_timetable.lessons):
            assert db['number'] == parser.number
            assert db['subject'] == parser.subject
            assert db['cabinet'] == parser.cabinet
            assert set(db['types']) == set(TypesLesson.from_parser_type_lesson(i).value for i in parser.types)
            assert db['gn'] == parser.group
            assert db['ts'] == parser.teacher
