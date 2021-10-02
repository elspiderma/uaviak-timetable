import datetime

import pytest

from db import Database
from db.structures import Departaments, TypesLesson


class TestDatabase:
    @pytest.mark.asyncio
    async def test_search(self, db_conn):
        query_search = Database(db_conn)
        groups = ('ГруППа 1', 'ГрУппа 2', 'Группа 3')

        for i in groups:
            await db_conn.fetch(f'INSERT INTO groups(number) VALUES ($1)', i)

        result1 = await query_search._search('груп', 'groups', 'number')
        result2 = await query_search._search('груПП', 'groups', 'number')
        result3 = await query_search._search('группа 2', 'groups', 'number')
        result4 = await query_search._search('груа1', 'groups', 'number', ignore_chars=('п', ' '))

        for r in (result1, result2):
            assert len(r) == 3

            for i, j in zip(groups, r):
                assert i == j['number']

        assert len(result3) == 1
        assert result3[0]['number'] == groups[1]

        assert len(result4) == 1
        assert result4[0]['number'] == groups[0]

    @pytest.mark.asyncio
    async def test_search_groups(self, db_conn):
        query_search = Database(db_conn)
        groups = ('19ис-1', '18ис-2', '20ис-1', '20ис-2', '20ис-3', '19трп1', '19трп2')

        for i in groups:
            await db_conn.fetch(f'INSERT INTO groups(number) VALUES ($1)', i)

        result1 = await query_search.search_groups('19ис-1')
        result2 = await query_search.search_groups('19ис1')
        result3 = await query_search.search_groups('19 И с 1')
        result4 = await query_search.search_groups('19ис')
        result5 = await query_search.search_groups('19трп')
        result6 = await query_search.search_groups('19трп-2')
        result7 = await query_search.search_groups('21ис')

        for i in (result1, result2, result3, result4):
            assert len(i) == 1
            assert i[0].number == groups[0]

        assert len(result5) == 2
        assert result5[0].number == groups[5]
        assert result5[1].number == groups[6]

        assert len(result6) == 1
        assert result6[0].number == groups[6]

        assert len(result7) == 0

    @pytest.mark.asyncio
    async def test_search_teachers(self, db_conn):
        query_search = Database(db_conn)
        teachers = ('Антропова О.А.', 'Брайцара А.А.', 'Брындина И.С')

        for i in teachers:
            await db_conn.fetch(f'INSERT INTO teachers(short_name) VALUES ($1)', i)

        result1 = await query_search.search_teachers('Антропова О.А.')
        result2 = await query_search.search_teachers('анТроПОва ОА')
        result3 = await query_search.search_teachers('антро')
        result4 = await query_search.search_teachers('бр')
        result5 = await query_search.search_teachers('п')

        for i in (result1, result2, result3):
            assert len(i) == 1
            assert i[0].short_name == teachers[0]

        assert len(result4) == 2
        assert result4[0].short_name == teachers[1]
        assert result4[1].short_name == teachers[2]

        assert len(result5) == 0

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
    async def test_search_by_id(self, db_conn):
        db = Database(db_conn)
        id_ = 42
        number_group = '19ис-1'
        await db_conn.fetch('INSERT INTO groups(id, number) VALUES ($1, $2)', 42, number_group)

        result1 = await db._search_by_id(id_, 'groups')
        result2 = await db._search_by_id(101, 'groups')

        assert result1['number'] == number_group
        assert result2 is None

    @pytest.mark.asyncio
    async def test_search_group_by_id(self, db_conn):
        db = Database(db_conn)
        id_ = 42
        number_group = '19ис-1'
        await db_conn.fetch('INSERT INTO groups(id, number) VALUES ($1, $2)', 42, number_group)

        result1 = await db.search_group_by_id(id_)
        result2 = await db.search_group_by_id(404)

        assert result1.number == number_group
        assert result2 is None

    @pytest.mark.asyncio
    async def test_search_teacher_by_id(self, db_conn):
        db = Database(db_conn)
        id_ = 42
        name_teacher = 'Брындина И.С.'
        await db.conn.fetch('INSERT INTO teachers(id, short_name) VALUES ($1, $2)', id_, name_teacher)

        result1 = await db.search_teacher_by_id(id_)
        result2 = await db.search_teacher_by_id(404)

        assert result1.short_name == name_teacher
        assert result2 is None

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
