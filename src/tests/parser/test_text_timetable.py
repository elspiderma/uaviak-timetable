import json

import pytest

from parser.text_timetable import TextTimetable, TypesLesson
from parser.structures import Lesson
import datetime


class TestTextTimetable:
    DATE = datetime.date(day=5, month=7, year=2021)
    TITLE = f'Расписание {DATE.strftime("%d.%m.%Y")} Понедельник (Дневное отделение)'
    ADDITIONAL_INFO = 'Дополнительная информация\nБла-Бла\nБла-Бла'
    LESSONS = [
        Lesson(
            number=3,
            subject='Предмет',
            cabinet='каб',
            types={TypesLesson.PRACTICAL},
            group='группа',
            teacher='Фамил И.Н.'
        ),
        Lesson(
            number=2,
            subject='Предмет',
            cabinet='каб',
            types={TypesLesson.EXAM, TypesLesson.SPLIT},
            group='группа',
            teacher='Фамил И.Н.'
        ),
        Lesson(
            number=1,
            subject='Производственная практика',
            cabinet='214*к',
            types={TypesLesson.PRACTICAL},
            group='18адс1',
            teacher='Кольцов В.А.'
        )
    ]
    LESSONS_TEXT = [
        f'{LESSONS[0].group} {LESSONS[0].number} {LESSONS[0].cabinet}{LESSONS[0].teacher} {LESSONS[0].subject} Практика',
        f'{LESSONS[1].group} {LESSONS[1].number} дрб {LESSONS[1].cabinet} {LESSONS[1].teacher} {LESSONS[1].subject} Экзамен',
        f'{LESSONS[2].group} {LESSONS[2].number} {LESSONS[2].cabinet} {LESSONS[2].teacher} {LESSONS[2].subject} Практика'
    ]

    TIMETABLE_TEXT = f"""{TITLE}

{ADDITIONAL_INFO}
------------------------------------------
{LESSONS_TEXT[0].replace(' ', ' ' * 10)}
{LESSONS_TEXT[1]}
{LESSONS_TEXT[2]}
"""

    def test_parse(self):
        text_timetable = TextTimetable.parse(self.TIMETABLE_TEXT)

        assert text_timetable.title == self.TITLE
        assert text_timetable.additional_info == self.ADDITIONAL_INFO
        for parsed_lesson, test_lesson in zip(text_timetable.lessons, self.LESSONS_TEXT):
            assert parsed_lesson == test_lesson

    def test_parse_text_ok(self):
        text_timetable = TextTimetable(self.TITLE, self.ADDITIONAL_INFO, self.LESSONS_TEXT)

        timetable = text_timetable.parse_text()

        assert timetable.additional_info == self.ADDITIONAL_INFO
        assert timetable.date == self.DATE
        for parsed_lesson, test_lesson in zip(timetable.lessons, self.LESSONS):
            assert parsed_lesson == test_lesson
