import asyncio

import pytest
import asyncpg
import os


def pytest_addoption(parser):
    parser.addoption('--ip', default='127.0.0.1', action='store', help='address test database')
    parser.addoption('--login', action='store', help='login test database')
    parser.addoption('--password', action='store', help='password test database')
    parser.addoption('--schema', action='store', help='schema test database')


@pytest.fixture()
def ip_db(request) -> str:
    return request.config.getoption("--ip")


@pytest.fixture()
def login_db(request) -> str:
    return request.config.getoption("--login")


@pytest.fixture()
def password_db(request) -> str:
    return request.config.getoption("--password")


@pytest.fixture()
def database_name() -> str:
    return f'pytest_db_{os.getpid()}'


@pytest.fixture()
def schema_db(request):
    with open(request.config.getoption("--schema"), 'r') as f:
        sql_schema = f.read()

    return sql_schema


@pytest.fixture(scope='function')
async def db_connection(ip_db, login_db, password_db, database_name, schema_db) -> asyncpg.Connection:
    sys_conn: asyncpg.Connection = await asyncpg.connect(host=ip_db, user=login_db, password=password_db)

    result = await sys_conn.fetch(
        'SELECT COUNT(datname) as count_db FROM pg_database WHERE datname = $1',
        database_name
    )
    count_db = int(result[0]['count_db'])
    if count_db == 1:  # Если БД уже существует, то удалям ее.
        await sys_conn.execute(f'DROP DATABASE {database_name}')

    # Создаем тестовую БД
    await sys_conn.execute(f'CREATE DATABASE {database_name}')

    conn: asyncpg.Connection = await asyncpg.connect(
        host=ip_db, user=login_db, password=password_db, database=database_name
    )
    await conn.execute(schema_db)
    await conn.execute('SET search_path TO public')
    yield conn
    await conn.close()

    await sys_conn.execute(f'DROP DATABASE {database_name}')
    await sys_conn.close()
