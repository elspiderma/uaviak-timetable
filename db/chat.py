from tortoise import fields
from tortoise.models import Model


class Chat(Model):
    class Meta:
        table = 'chats'

    id = fields.IntField(pk=True)
    id_vk = fields.IntField()
    is_photo = fields.BooleanField(default=True)
