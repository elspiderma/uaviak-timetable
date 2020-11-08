import typing

from tortoise import fields
from tortoise.models import Model

if typing.TYPE_CHECKING:
    from db import Timetable


class Teacher(Model):
    class Meta:
        table = 'teachers'

    id = fields.IntField(pk=True)
    short_name = fields.CharField(max_length=100)
    full_name = fields.CharField(max_length=100, null=True)

    lessons: fields.ReverseRelation['Timetable']

    def __repr__(self):
        return f'<{self.short_name}>'
