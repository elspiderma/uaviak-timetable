from tortoise import fields
from tortoise.models import Model


class NotifyTeacher(Model):
    class Meta:
        table = 'notify_teacher'

    id = fields.IntField(pk=True)
    id_chat = fields.ForeignKeyField('models.Chat', on_delete=fields.CASCADE)
    teacher = fields.ForeignKeyField('models.Teacher', on_delete=fields.CASCADE)


class NotifyGroup(Model):
    class Meta:
        table = 'notify_group'

    id = fields.IntField(pk=True)
    id_chat = fields.ForeignKeyField('models.Chat', on_delete=fields.CASCADE)
    group = fields.ForeignKeyField('models.Group', on_delete=fields.CASCADE)
