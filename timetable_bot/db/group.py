import typing

from tortoise import fields

import db
from db.search_abc import SearchABC

if typing.TYPE_CHECKING:
    from datetime import date

if typing.TYPE_CHECKING:
    from db import Lesson


class Group(SearchABC):
    class Meta:
        table = 'groups'

    IGNORE_CHAR = ['-', ' ']

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique=True)

    lessons: fields.ReverseRelation["Lesson"]

    def __repr__(self):
        return f'<{self.title}>'

    @property
    def _search_field(self):
        return self.title

    def get_timetable(self, date: 'date'):
        return db.Lesson.filter(date=date, group=self).order_by('number').all()
