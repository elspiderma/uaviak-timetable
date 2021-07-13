from uaviak_parser.text_timetable import TextTimetable


class TestTextTimetable:
    def test_parse(self, test_timetable):
        text_timetable = TextTimetable.parse(test_timetable.text)

        assert text_timetable.title == test_timetable.text.splitlines()[0]

    def test_parse_text_ok(self, test_timetable):
        text_timetable = TextTimetable.parse(test_timetable.text)

        timetable = text_timetable.parse_text()

        assert timetable.additional_info == test_timetable.structure.additional_info
        assert timetable.date == test_timetable.structure.date
        for parsed_lesson, test_lesson in zip(timetable.lessons, test_timetable.structure.lessons):
            assert parsed_lesson == test_lesson
