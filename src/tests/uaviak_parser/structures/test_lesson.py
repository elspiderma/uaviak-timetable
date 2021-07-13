from copy import copy

from uaviak_parser.structures import Lesson, TypesLesson


class TestLesson:
    def test_eq_true(self):
        l1 = Lesson(
            number=1,
            subject='subject',
            cabinet='333',
            types={TypesLesson.SPLIT, TypesLesson.EXAM},
            group='12kd-2',
            teacher='Test T.T.'
        )
        l2 = Lesson(
            number=1,
            subject='subject',
            cabinet='333',
            types={TypesLesson.SPLIT, TypesLesson.EXAM},
            group='12kd-2',
            teacher='Test T.T.'
        )

        assert l1 == l2

    def test_eq_false(self):
        l1 = Lesson(
            number=1,
            subject='subject',
            cabinet='333',
            types=set(),
            group='12kd-2',
            teacher='Test T.T.'
        )

        for attr in l1.__dict__:
            l1_copy = copy(l1)
            setattr(l1_copy, attr, 'editer')
            assert l1_copy != l1
