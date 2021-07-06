import json

import pytest
from aioresponses import aioresponses

from parser import HtmlTimetable
from parser.exceptions import GetHtmlError
from tests.conftest import get_resources


class TestHtmlTimetable:
    TIMETABLE_HTML = """<!DOCTYPE html>
<html>
<head>
</head>
<div class=mobile-button></div>
<body>
<div class="gblock topnav"></div>
<div class="page-wrap scrolling gblock">
<div class=gwrap>
<div class=scrolling-text-wrap>
<div class="scrolling-text pos1">
<div class=title>
Расписание заочного отделения
</div>
Расписание заочное<br><br>
----------------------------------------------------------------------------------------<br>
Пара 1<br>
Пара 2<br>
</div>
<div class="scrolling-text pos2">
<div class=title>
Расписание очного отделения
</div>
Расписание очное<br><br>
Пара1<br>
Пара2<br>
</div>
</div>
</div>
</div>
</body>
</html>"""
    TIMETABLE_TEXT = [
        '\n\nРасписание заочное\n----------------------------------------------------------------------------------------\nПара 1\nПара 2\n',
        '\n\nРасписание очное\nПара1\nПара2\n'
    ]

    @pytest.mark.asyncio
    async def test_load_ok(self):
        with aioresponses() as m:
            m.get(HtmlTimetable.TIMETABLE_URL, status=200, body=self.TIMETABLE_HTML)

            loaded_html = await HtmlTimetable.load()

            assert loaded_html == self.TIMETABLE_HTML

    @pytest.mark.asyncio
    async def test_load_error(self):
        with pytest.raises(GetHtmlError):
            with aioresponses() as m:
                m.get(HtmlTimetable.TIMETABLE_URL, status=500)

                await HtmlTimetable.load()

    def test_parse(self):
        html_timetable = HtmlTimetable(self.TIMETABLE_HTML)

        text_timetable = html_timetable.parse_html()

        assert text_timetable[0] == self.TIMETABLE_TEXT[0]
        assert text_timetable[1] == self.TIMETABLE_TEXT[1]

    def test_qe(self):
        text_ok = 'hello world'

        html_timetable_ok = HtmlTimetable(text_ok)
        html_timetable_fail = HtmlTimetable('hi')

        assert html_timetable_ok == text_ok
        assert html_timetable_fail != text_ok
