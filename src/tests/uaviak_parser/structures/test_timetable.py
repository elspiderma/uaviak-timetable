from copy import copy
import datetime

from uaviak_parser.structures import Lesson, Timetable, Departaments


class TestTimetable:
    def test_eq_true(self):
        lessons = [
            Lesson(
                number=1,
                subject='subject',
                cabinet='333',
                types=set(),
                group='12kd-2',
                teacher='Test T.T.'
            ),
            Lesson(
                number=2,
                subject='subject',
                cabinet='333',
                types=set(),
                group='12kd-2',
                teacher='Test T.T.'
            )
        ]

        t1 = Timetable(
            additional_info='test',
            date=datetime.date.today(),
            departament=Departaments.FULL_TIME,
            lessons=lessons.copy()
        )
        t2 = Timetable(
            additional_info='test',
            date=datetime.date.today(),
            departament=Departaments.FULL_TIME,
            lessons=lessons.copy()
        )

        assert t1 == t2

    def test_eq_false(self):
        lessons = [
            Lesson(
                number=1,
                subject='subject',
                cabinet='333',
                types=set(),
                group='12kd-2',
                teacher='Test T.T.'
            ),
            Lesson(
                number=2,
                subject='subject1',
                cabinet='333',
                types=set(),
                group='12kd-2',
                teacher='Test T.T.'
            )
        ]

        t1 = Timetable(
            additional_info='test',
            date=datetime.date.today(),
            departament=Departaments.FULL_TIME,
            lessons=lessons.copy()
        )

        t2 = copy(t1)
        t2.lessons = t2.lessons.copy()
        del t2.lessons[0]

        t3 = copy(t1)
        t3.lessons = t3.lessons.copy()
        t3.lessons.append(Lesson(
                number=3,
                subject='subject',
                cabinet='333',
                types=set(),
                group='12kd-2',
                teacher='Test T.T.'
        ))

        t3 = copy(t1)
        t3.additional_info = 'dfksdf'

        assert t1 != t2
        assert t1 != t3
        assert t2 != t3
