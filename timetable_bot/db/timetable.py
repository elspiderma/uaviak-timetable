import typing

from tortoise import fields
from tortoise.models import Model

if typing.TYPE_CHECKING:
    from db import Group, Teacher


class Timetable(Model):
    class Meta:
        table = 'timetable'

    id = fields.IntField(pk=True)
    department = fields.IntField()
    date = fields.DateField()
    group: fields.ForeignKeyRelation['Group'] = fields.ForeignKeyField(
        'models.Group', related_name='lessons', on_delete=fields.CASCADE
    )
    number = fields.IntField()
    cabinet = fields.CharField(20)
    teacher: fields.ForeignKeyRelation['Teacher'] = fields.ForeignKeyField(
        'models.Teacher', related_name='lessons', on_delete=fields.CASCADE
    )
    subject = fields.CharField(100)
    is_splitting = fields.BooleanField()
    is_practice = fields.BooleanField()
    is_consultations = fields.BooleanField()
    is_exam = fields.BooleanField()
