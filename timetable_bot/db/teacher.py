import typing

from tortoise import fields

from db.search_abc import SearchABC
import db

if typing.TYPE_CHECKING:
    from datetime import date

if typing.TYPE_CHECKING:
    from db import Lesson


class Teacher(SearchABC):
    class Meta:
        table = 'teachers'

    IGNORE_CHAR = ['.', ' ']

    id = fields.IntField(pk=True)
    short_name = fields.CharField(max_length=100)
    full_name = fields.CharField(max_length=100, null=True)

    lessons: fields.ReverseRelation['Lesson']

    def __repr__(self):
        return f'<{self.short_name}>'

    @property
    def _search_field(self):
        return self.short_name

    def get_timetable(self, date: 'date'):
        return db.Lesson.filter(date=date, group=self).order_by('number').all()
