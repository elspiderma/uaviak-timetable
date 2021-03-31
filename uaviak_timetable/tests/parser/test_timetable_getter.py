import pytest

from uaviak_timetable.structures import Departament
from uaviak_timetable.exceptions import GetHtmlError
from uaviak_timetable.parser import TimetableGetter
from aioresponses import aioresponses


@pytest.fixture(scope='session')
def timetable_html() -> str:
    from os.path import abspath, join, dirname
    path_html = join(dirname(abspath(__file__)), 'resources/timetable_html.html')

    with open(path_html, 'r') as f:
        return f.read()


@pytest.fixture(scope='session')
def timetables_text() -> list[str]:
    import json

    from os.path import abspath, join, dirname
    path_html = join(dirname(abspath(__file__)), 'resources/timetable_text.json')

    with open(path_html) as f:
        return json.load(f)


class TestTimetableGetter:
    @pytest.mark.asyncio
    async def test_load_html(self, timetable_html):
        with aioresponses() as m:
            m.get(TimetableGetter.TIMETABLE_URL, status=200, body=timetable_html)
            loaded_html = await TimetableGetter._load_html()

            assert loaded_html == timetable_html

        with pytest.raises(GetHtmlError) as e:
            with aioresponses() as m:
                m.get(TimetableGetter.TIMETABLE_URL, status=500)
                await TimetableGetter._load_html()

        assert e.value.exceptions.code == 500

    def test_parse_html(self, timetable_html, timetables_text):
        parsed_html = TimetableGetter._parse_html(timetable_html)

        assert len(parsed_html) == 2
        for parsed, text in zip(parsed_html, timetables_text):
            assert parsed == text

    def test_prepare_timetable_text(self, timetables_text):
        title, info, lessons = TimetableGetter._prepare_timetable_text(timetables_text[0])
        assert title == 'Расписание 23.03.2021 Вторник (Заочное отделение)'
        assert info == ''
        assert len(lessons) == 4
        assert lessons[0] == '18ктиз 1 705л Ларионова Л.Ф. Информационные технологии в пр'

        title, info, lessons = TimetableGetter._prepare_timetable_text(timetables_text[1])
        assert title == 'Расписание 23.03.2021 Вторник (Дневное отделение)'
        assert info == 'Режим работы на 24.03.2021\n1 пара 8.15 - 9.15\n2 пара 9.25 - 10.25\n3 пара 10.35 - 11.35'
        assert len(lessons) == 220
        assert lessons[0] == '17адс1 1 214*кКольцов В.А. Учебная практика Практика'

    @pytest.mark.asyncio
    async def test_load(self, timetable_html):
        with aioresponses() as m:
            m.get(TimetableGetter.TIMETABLE_URL, status=200, body=timetable_html)

            timetables = await TimetableGetter.load()
            assert timetables[0].departament == Departament.CORRESPONDENCE
            assert timetables[0].additional_info == ''
            assert len(timetables[0].lessons) == 4

            assert timetables[1].departament == Departament.FULL_TIME
            assert timetables[1].additional_info == \
                   'Режим работы на 24.03.2021\n1 пара 8.15 - 9.15\n2 пара 9.25 - 10.25\n3 пара 10.35 - 11.35'
            assert len(timetables[1].lessons) == 220
