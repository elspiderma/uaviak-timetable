from tortoise import fields
from tortoise.models import Model


class Timetable(Model):
    class Meta:
        table = 'timetable'

    id = fields.IntField(pk=True)
    date = fields.DateField()
    group = fields.ForeignKeyField('models.Group', related_name='timetable', on_delete=fields.CASCADE)
    number = fields.IntField()
    cabinet = fields.CharField(20)
    teacher = fields.ForeignKeyField('models.Teacher', related_name='timetable', on_delete=fields.CASCADE)
    subject = fields.CharField(100)
    is_splitting = fields.BooleanField()
    is_practice = fields.BooleanField()
    is_consultations = fields.BooleanField()
    is_exam = fields.BooleanField()
