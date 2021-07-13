import pytest

from db.structures import TypesLesson
from uaviak_parser.structures import TypesLesson as ua_TypesLesson


class TestDepartaments:
    @pytest.mark.asyncio
    async def test_sync_db(self, db_conn):
        values_db = await db_conn.fetch(
            """SELECT pg_enum.enumlabel FROM pg_enum
            INNER JOIN pg_type pt on pg_enum.enumtypid = pt.oid
            WHERE pt.typname = 'TypesLesson'""")

        type_no_db = list(TypesLesson)
        for i in values_db:
            type_no_db.remove(TypesLesson(i['enumlabel']))

        # Проверяем, что все значение, которые могут быть в python-enum есть и в БД.
        assert len(type_no_db) == 0

    def test_from_parser_departaments(self):
        type_no_db = list(TypesLesson)
        for i in ua_TypesLesson:
            type_no_db.remove(TypesLesson.from_parser_type_lesson(i))

        assert len(type_no_db) == 0
