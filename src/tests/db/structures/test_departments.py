import pytest

from db.structures import Departaments
from uaviak_parser.structures import Departaments as ua_Departaments


class TestDepartaments:
    @pytest.mark.asyncio
    async def test_sync_db(self, db_conn):
        values_db = await db_conn.fetch(
            """SELECT pg_enum.enumlabel FROM pg_enum
            INNER JOIN pg_type pt on pg_enum.enumtypid = pt.oid
            WHERE pt.typname = 'Departaments'""")

        departaments_no_db = list(Departaments)
        for i in values_db:
            departaments_no_db.remove(Departaments(i['enumlabel']))

        # Проверяем, что все значение, которые могут быть в python-enum есть и в БД.
        assert len(departaments_no_db) == 0

    def test_from_parser_departaments(self):
        departaments_no_parser = list(Departaments)
        for i in ua_Departaments:
            departaments_no_parser.remove(Departaments.from_parser_departaments(i))

        assert len(departaments_no_parser) == 0
