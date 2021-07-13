import pytest

from config import Configuration, IniReader
from db import ConnectionKeeper, ConnectionNotInit


@pytest.fixture(scope='function')
def configuration_db(login_db, password_db, database_name, ip_db) -> Configuration:
    ini_reader = IniReader()
    ini_reader.set('postgres', 'login', login_db)
    ini_reader.set('postgres', 'password', password_db)
    ini_reader.set('postgres', 'ip', ip_db)
    ini_reader.set('postgres', 'database', database_name)

    return Configuration(ini_reader)


class TestConnectionKeeper:
    def test_get_connection_error(self):
        with pytest.raises(ConnectionNotInit):
            ConnectionKeeper.get_connection()

    @pytest.mark.asyncio
    async def test_close_connection_error(self):
        with pytest.raises(ConnectionNotInit):
            await ConnectionKeeper.close_connection()

    @pytest.mark.asyncio
    async def test_init_connection(self, login_db, password_db, database_name, ip_db):
        assert ConnectionKeeper._connection is None
        await ConnectionKeeper.init_connection(login_db, password_db, database_name, ip_db)

        assert ConnectionKeeper._connection is not None

        await ConnectionKeeper.close_connection()
        assert ConnectionKeeper._connection is None

    @pytest.mark.asyncio
    async def test_init_connection_from_config(self, configuration_db):
        assert ConnectionKeeper._connection is None
        await ConnectionKeeper.init_connection_from_config(configuration_db)

        assert ConnectionKeeper._connection is not None

        await ConnectionKeeper.close_connection()
        assert ConnectionKeeper._connection is None
