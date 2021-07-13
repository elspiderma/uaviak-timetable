import os
from typing import Optional

import asyncpg
import pytest
from constants import SQL_PATH
import string
import random


def pytest_addoption(parser):
    parser.addoption('--ip', default='127.0.0.1', action='store', help='address test database')
    parser.addoption('--login', action='store', help='login test database', required=True)
    parser.addoption('--password', action='store', help='password test database', required=True)
    parser.addoption('--prefix-name', default='pytest_db', action='store', help='password test database')


class FakeInput:
    def __init__(self, answer: str):
        self.answer = answer
        self.prompt = None

    def input(self, prompt: Optional[str] = None) -> str:
        self.prompt = prompt
        return self.answer

    def __call__(self, *args, **kwargs) -> str:
        return self.input(*args, **kwargs)


@pytest.fixture(scope='function')
def random_string():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(5))


@pytest.fixture()
def ip_db(request) -> str:
    return request.config.getoption("--ip")


@pytest.fixture()
def login_db(request) -> str:
    return request.config.getoption("--login")


@pytest.fixture()
def password_db(request) -> str:
    return request.config.getoption("--password")


@pytest.fixture(scope='function')
async def database_name(ip_db, login_db, password_db, request, random_string) -> str:
    name = f'{request.config.getoption("--prefix-name")}_{request.node.name}_{random_string}'

    sys_conn: asyncpg.Connection = await asyncpg.connect(host=ip_db, user=login_db, password=password_db)

    # Создаем тестовую БД
    await sys_conn.execute(f'CREATE DATABASE {name};')

    yield name

    await sys_conn.execute(f'DROP DATABASE {name};')
    await sys_conn.close()


@pytest.fixture()
def schema_db():
    with open(os.path.join(SQL_PATH, 'shema.sql'), 'r') as f:
        sql_schema = f.read()

    return sql_schema


@pytest.fixture(scope='function')
async def db_conn(ip_db, login_db, password_db, database_name, schema_db) -> asyncpg.Connection:
    conn: asyncpg.Connection = await asyncpg.connect(
        host=ip_db, user=login_db, password=password_db, database=database_name
    )
    await conn.execute(schema_db)
    await conn.execute('SET search_path TO public;')

    yield conn

    await conn.close()
