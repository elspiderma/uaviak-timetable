import datetime
import os
import random
import string
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

import asyncpg
import pytest

import uaviak_parser.structures as ua_structures
from constants import SQL_PATH


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


@pytest.fixture(scope='session')
def ip_db(request) -> str:
    return request.config.getoption("--ip")


@pytest.fixture(scope='session')
def login_db(request) -> str:
    return request.config.getoption("--login")


@pytest.fixture(scope='session')
def password_db(request) -> str:
    return request.config.getoption("--password")


@pytest.fixture(scope='function')
async def database_name(ip_db, login_db, password_db, request, random_string) -> str:
    """Генерирут имя БД и создает ее в СУБД.

    Returns:
        Имя БД.
    """
    name = f'{request.config.getoption("--prefix-name")}_{request.node.name}_{random_string}'

    sys_conn: asyncpg.Connection = await asyncpg.connect(host=ip_db, user=login_db, password=password_db)

    # Создаем тестовую БД
    await sys_conn.execute(f'CREATE DATABASE {name};')

    yield name

    await sys_conn.execute(f'DROP DATABASE {name};')
    await sys_conn.close()


@pytest.fixture()
def schema_db():
    with open(os.path.join(SQL_PATH, 'scheme.sql'), 'r') as f:
        sql_schema = f.read()

    return sql_schema


@pytest.fixture(scope='function')
async def db_conn(ip_db, login_db, password_db, database_name, schema_db) -> asyncpg.Connection:
    """Создает подключение к БД.

    Returns:
        Коннекшен к БД.
    """
    conn: asyncpg.Connection = await asyncpg.connect(
        host=ip_db, user=login_db, password=password_db, database=database_name
    )
    await conn.execute(schema_db)
    await conn.execute('SET search_path TO public;')

    yield conn

    await conn.close()


@dataclass
class RandomTimetableTest:
    structure: ua_structures.Timetable
    text: str
    html: str


def generate_parser_timetable(date: datetime.date, departament: ua_structures.Departaments) -> ua_structures.Timetable:
    """Генерирует рандомное расписание с сайта.

    Returns:
        Рандомное расписание.
    """
    def rand_str(max_length: int, min_length: int = 1):
        length = random.randint(min_length, max_length)

        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    groups = [rand_str(4) for _ in range(5)]
    teacher = [f'{rand_str(15, 6)} F.F.' for _ in range(5)]

    lessons = []
    for i in range(100):
        types_lesson = set()
        if random.randint(0, 1):
            types_lesson.add(ua_structures.TypesLesson.SPLIT)
        if random.randint(0, 1):
            types_lesson.add(random.choice(tuple(ua_structures.TypesLesson)))

        lessons.append(ua_structures.Lesson(
            number=random.randint(1, 5),
            subject=rand_str(50),
            cabinet=rand_str(3) if random.randint(0, 1) else None,
            types=types_lesson,
            group=random.choice(groups),
            teacher=random.choice(teacher)
        ))

    return ua_structures.Timetable(
        additional_info=rand_str(200),
        date=date,
        departament=departament,
        lessons=lessons
    )


def generate_text_for_timetable(timetable: ua_structures.Timetable) -> str:
    def random_space() -> str:
        return ' ' * random.randint(1, 5)

    result = ''
    result += f'Расписание {timetable.date.strftime("%d.%m.%Y")} Понедельник ({"Дневное" if timetable.departament is ua_structures.Departaments.FULL_TIME else "Заочное"} отделение)\n'
    result += timetable.additional_info + '\n'

    result += '-------------------------------------------\n'

    for i in timetable.lessons:
        lesson_line_component: list[str] = []
        lesson_line_component.append(i.group)
        lesson_line_component.append(str(i.number))

        if ua_structures.TypesLesson.SPLIT in i.types:
            lesson_line_component.append('дрб')

        if i.cabinet:
            lesson_line_component.append(i.cabinet)

        lesson_line_component.append(i.teacher)
        lesson_line_component.append(i.subject)

        if ua_structures.TypesLesson.EXAM in i.types:
            lesson_line_component.append('Экзамен')
        elif ua_structures.TypesLesson.PRACTICAL in i.types:
            lesson_line_component.append('Практика')
        elif ua_structures.TypesLesson.CONSULTATION in i.types:
            lesson_line_component.append('Консульт')

        lesson_line = ''
        for comp in lesson_line_component:
            lesson_line += comp
            lesson_line += random_space()

        result += lesson_line + '\n'

        if random.randint(1, 4) == 1:
            result += '-------------------------------------------\n'

    return result


def generate_html_timetable(text: str) -> str:
    text_html = text.replace('\n', '<br>\n')
    return f"""<!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <div class="scrolling-text pos2">
    <div class=title>
    Расписание очного отделения
    </div>
    {text_html}
    </div>
    </body>
    </html>"""


@pytest.fixture(scope='session')
def test_timetable() -> RandomTimetableTest:
    structure = generate_parser_timetable(datetime.date.today(), random.choice(tuple(ua_structures.Departaments)))
    text = generate_text_for_timetable(structure)
    html = generate_html_timetable(text)
    return RandomTimetableTest(structure, text, html)
