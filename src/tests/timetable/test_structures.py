import datetime

import pytest

from timetable.exceptions import ParseLessonError, ParseTimetableError
from timetable.structures import LessonParsed, TypesLesson, TimetableParsed, Departament


class TestLessonParsed:
    def test_parse(self):
        lesson_parsed = LessonParsed.parse('17адс1 1 дрб 214*кКольцов В.А. Учебная практика Практика')
        assert lesson_parsed.group == '17адс1'
        assert lesson_parsed.number == 1
        assert lesson_parsed.cabinet == '214*к'
        assert lesson_parsed.teacher == 'Кольцов В.А.'
        assert lesson_parsed.subject == 'Учебная практика'
        assert lesson_parsed.types == [TypesLesson.SPLIT, TypesLesson.PRACTICAL]

        lesson_parsed = LessonParsed.parse('группа 5 каб Преп И.Н. Название предмета Экзамен')
        assert lesson_parsed.group == 'группа'
        assert lesson_parsed.number == 5
        assert lesson_parsed.cabinet == 'каб'
        assert lesson_parsed.teacher == 'Преп И.Н.'
        assert lesson_parsed.subject == 'Название предмета'
        assert lesson_parsed.types == [TypesLesson.EXAM]

        lesson_parsed = LessonParsed.parse('группа 5 каб Преп И.Н. Название предмета')
        assert lesson_parsed.group == 'группа'
        assert lesson_parsed.number == 5
        assert lesson_parsed.cabinet == 'каб'
        assert lesson_parsed.teacher == 'Преп И.Н.'
        assert lesson_parsed.subject == 'Название предмета'
        assert lesson_parsed.types == []

        lesson_parsed = LessonParsed.parse('18ам-1 3 402*кТитова Ю.А. Литература')
        assert lesson_parsed.group == '18ам-1'
        assert lesson_parsed.number == 3
        assert lesson_parsed.cabinet == '402*к'
        assert lesson_parsed.teacher == 'Титова Ю.А.'
        assert lesson_parsed.subject == 'Литература'
        assert lesson_parsed.types == []

        with pytest.raises(ParseLessonError) as e:
            LessonParsed.parse('неправильное рассписание')

        assert e.value.line == 'неправильное рассписание'


class TestTimetableParsed:
    def test_parse(self):
        lessons = [
            '17адс1 1 214*кКольцов В.А. Учебная практика Практика',
            '18бсп1 3 дрб 322л Рябушко А.В. Информационные технологии в пр'
        ]
        lessons_parsed = [
            LessonParsed(group='17адс1', number=1, cabinet='214*к', teacher='Кольцов В.А.',
                         subject='Учебная практика', types=[TypesLesson.PRACTICAL]),
            LessonParsed(group='18бсп1', number=3, cabinet='322л', teacher='Рябушко А.В.',
                         subject='Информационные технологии в пр', types=[TypesLesson.SPLIT])
        ]

        info = 'Всякая разная инфа'

        parsed_timetable = TimetableParsed.parse('Расписание 23.03.2021 Вторник (Заочное отделение)', info, lessons)
        assert parsed_timetable.date == datetime.date(2021, 3, 23)
        assert parsed_timetable.departament == Departament.CORRESPONDENCE
        assert parsed_timetable.lessons == lessons_parsed
        assert parsed_timetable.additional_info == info

        parsed_timetable = TimetableParsed.parse('Расписание на 23.03.2021 Вторник (Заочное отделение)', '', lessons)
        assert parsed_timetable.date == datetime.date(2021, 3, 23)
        assert parsed_timetable.departament == Departament.CORRESPONDENCE
        assert parsed_timetable.lessons == lessons_parsed
        assert parsed_timetable.additional_info is None

        with pytest.raises(ParseTimetableError) as e:
            TimetableParsed.parse('Расписание на 23.30.2021 Вторник (Заочное отделение)', '', lessons)
        assert e.value.title == 'Расписание на 23.30.2021 Вторник (Заочное отделение)'
        assert e.value.lessons == lessons
        assert e.value.info == ''

        with pytest.raises(ParseTimetableError) as e:
            TimetableParsed.parse('неправильный загаловок', info, lessons)
        assert e.value.title == 'неправильный загаловок'
        assert e.value.lessons == lessons
        assert e.value.info == info
