from tortoise.models import Model
from tortoise import fields


class Chat(Model):
    class Meta:
        table = 'chats'

    id = fields.IntField(pk=True)
    id_vk = fields.IntField()
    is_photo = fields.BooleanField(default=True)
