import typing

from tortoise import fields
from tortoise.models import Model

if typing.TYPE_CHECKING:
    from db import Timetable


class Group(Model):
    class Meta:
        table = 'groups'

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique=True)

    lessons: fields.ReverseRelation["Timetable"]

    def __repr__(self):
        return f'<{self.title}>'
