from tortoise import fields
from tortoise.models import Model


class NotifyTeacher(Model):
    class Meta:
        table = 'notify_teacher'

    id = fields.IntField(pk=True)
    id_chat = fields.ForeignKeyField('models.Chat')
    teacher = fields.ForeignKeyField('models.Teacher')


class NotifyGroup(Model):
    class Meta:
        table = 'notify_group'

    id = fields.IntField(pk=True)
    id_chat = fields.ForeignKeyField('models.Chat')
    group = fields.ForeignKeyField('models.Group')
