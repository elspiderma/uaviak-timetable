import pytest
from aioresponses import aioresponses

from uaviak_parser import HtmlTimetable
from uaviak_parser.exceptions import GetHtmlError


class TestHtmlTimetable:
    @pytest.mark.asyncio
    async def test_load_ok(self, test_timetable):
        with aioresponses() as m:
            m.get(HtmlTimetable.TIMETABLE_URL, status=200, body=test_timetable.html)

            loaded_html = await HtmlTimetable.load()

            assert loaded_html == test_timetable.html

    @pytest.mark.asyncio
    async def test_load_error(self):
        with pytest.raises(GetHtmlError):
            with aioresponses() as m:
                m.get(HtmlTimetable.TIMETABLE_URL, status=500)

                await HtmlTimetable.load()

    def test_parse(self, test_timetable):
        html_timetable = HtmlTimetable(test_timetable.html)

        text_timetable = html_timetable.parse_html()

        assert text_timetable[0].strip() == test_timetable.text.strip()

    def test_qe(self):
        text_ok = 'hello world'

        html_timetable_ok = HtmlTimetable(text_ok)
        html_timetable_fail = HtmlTimetable('hi')

        assert html_timetable_ok == text_ok
        assert html_timetable_fail != text_ok
